from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_adverse_event.choices import STUDY_DRUG_RELATIONSHIP
from edc_adverse_event.constants import (
    DEFINITELY_RELATED,
    DISCHARGED,
    INPATIENT,
    NOT_RELATED,
    POSSIBLY_RELATED,
    PROBABLY_RELATED,
    UNLIKELY_RELATED,
)
from edc_constants.constants import (
    CONTROL,
    DECEASED,
    INTERVENTION,
    NO,
    NOT_APPLICABLE,
    UNKNOWN,
    YES,
)
from edc_constants.utils import get_display
from edc_reportable import GRADE3, GRADE4, GRADE5
from edc_utils import get_utcnow_as_date

from effect_ae.choices import INPATIENT_STATUSES
from effect_ae.form_validators import AeInitialFormValidator
from effect_ae.models import AeInitial
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin


@tag("ae")
class TestAeInitialFormValidation(EffectTestCaseMixin, TestCase):
    form_validator_cls = AeInitialFormValidator
    form_validator_model_cls = AeInitial

    inpatient_statuses = [choice[0] for choice in INPATIENT_STATUSES]
    study_drugs = ["flucon", "flucyt"]
    study_drug_relationships_choices = [choice[0] for choice in STUDY_DRUG_RELATIONSHIP]

    def setUp(self) -> None:
        super().setUp()

        # Patch, to allow assumption participant on intervention arm for all
        # tests (unless explicitly overridden)
        assignment_patcher = patch(
            "effect_ae.form_validators.ae_initial.get_assignment_for_subject"
        )
        self.addCleanup(assignment_patcher.stop)
        self.mock_get_assignment_for_subject = assignment_patcher.start()
        self.mock_get_assignment_for_subject.return_value = INTERVENTION

        assignment_descr_patcher = patch(
            "effect_ae.form_validators.ae_initial.get_assignment_description_for_subject"
        )
        self.addCleanup(assignment_descr_patcher.stop)
        self.mock_get_assignment_description_for_subject = assignment_descr_patcher.start()
        self.mock_get_assignment_description_for_subject.return_value = (
            "2 weeks fluconazole plus flucytosine"
        )

    def test_date_admitted_required_if_patient_admitted(self):
        cleaned_data = {"patient_admitted": YES, "date_admitted": None}
        self.assertFormValidatorError(
            field="date_admitted",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        cleaned_data.update({"date_admitted": get_utcnow_as_date()})
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_date_admitted_not_required_if_patient_not_admitted(self):
        cleaned_data = {
            "patient_admitted": NO,
            "date_admitted": get_utcnow_as_date(),
        }
        self.assertFormValidatorError(
            field="date_admitted",
            expected_msg="This field is not required",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        cleaned_data.update({"date_admitted": None})
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_inpatient_status_applicable_if_patient_admitted(self):
        cleaned_data = {
            "ae_grade": GRADE3,
            "patient_admitted": YES,
            "date_admitted": get_utcnow_as_date(),
            "inpatient_status": NOT_APPLICABLE,
        }
        self.assertFormValidatorError(
            field="inpatient_status",
            expected_msg="This field is applicable",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        for status in [value for value in self.inpatient_statuses if value != NOT_APPLICABLE]:
            with self.subTest(status=status):
                cleaned_data.update(
                    {
                        "ae_grade": GRADE5 if status == DECEASED else GRADE3,
                        "inpatient_status": status,
                        "date_discharged": (
                            get_utcnow_as_date() if status == DISCHARGED else None
                        ),
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_inpatient_status_not_applicable_if_patient_not_admitted(self):
        for status in [value for value in self.inpatient_statuses if value != NOT_APPLICABLE]:
            with self.subTest(status=status):
                cleaned_data = {"patient_admitted": NO, "inpatient_status": status}
                self.assertFormValidatorError(
                    field="inpatient_status",
                    expected_msg="This field is not applicable",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

        cleaned_data = {"patient_admitted": NO, "inpatient_status": NOT_APPLICABLE}
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_inpatient_status_deceased_invalid_if_not_g5(self):
        for grade in [GRADE3, GRADE4]:
            with self.subTest(grade=grade):
                cleaned_data = {
                    "ae_grade": grade,
                    "patient_admitted": YES,
                    "date_admitted": get_utcnow_as_date(),
                    "inpatient_status": DECEASED,
                }
                self.assertFormValidatorError(
                    field="inpatient_status",
                    expected_msg=(
                        "Invalid. Status cannot be 'Died during hospitalization' "
                        "if severity of AE is not 'Grade 5 - Death'"
                    ),
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_inpatient_status_deceased_valid_if_g5(self):
        cleaned_data = {
            "ae_grade": GRADE5,
            "patient_admitted": YES,
            "date_admitted": get_utcnow_as_date(),
            "inpatient_status": DECEASED,
        }
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_inpatient_status_inpatient_invalid_if_g5(self):
        cleaned_data = {
            "ae_grade": GRADE5,
            "patient_admitted": YES,
            "date_admitted": get_utcnow_as_date(),
            "inpatient_status": INPATIENT,
        }
        self.assertFormValidatorError(
            field="inpatient_status",
            expected_msg=(
                "Invalid. Status cannot be 'Currently an inpatient' "
                "if severity of AE is 'Grade 5 - Death'"
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_inpatient_status_inpatient_valid_if_not_g5(self):
        for grade in [GRADE3, GRADE4]:
            with self.subTest(grade=grade):
                cleaned_data = {
                    "ae_grade": grade,
                    "patient_admitted": YES,
                    "date_admitted": get_utcnow_as_date(),
                    "inpatient_status": INPATIENT,
                }
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_date_discharged_required_if_patient_discharged(self):
        cleaned_data = {
            "patient_admitted": YES,
            "date_admitted": get_utcnow_as_date(),
            "inpatient_status": DISCHARGED,
            "date_discharged": None,
        }
        self.assertFormValidatorError(
            field="date_discharged",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        cleaned_data.update({"date_discharged": get_utcnow_as_date()})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_date_discharged_not_required_if_patient_not_discharged(self):
        non_discharged_statuses = [
            value
            for value in self.inpatient_statuses
            if value != DISCHARGED and value != NOT_APPLICABLE
        ]
        for status in non_discharged_statuses:
            with self.subTest(status=status):
                cleaned_data = {
                    "ae_grade": GRADE5 if status == DECEASED else GRADE4,
                    "patient_admitted": YES,
                    "date_admitted": get_utcnow_as_date(),
                    "inpatient_status": status,
                    "date_discharged": get_utcnow_as_date(),
                }
                self.assertFormValidatorError(
                    field="date_discharged",
                    expected_msg="This field is not required",
                    form_validator=self.validate_form_validator(cleaned_data),
                )
                cleaned_data.update({"date_discharged": None})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_date_discharged_not_required_if_patient_not_admitted(self):
        cleaned_data = {
            "patient_admitted": NO,
            "date_admitted": None,
            "inpatient_status": NOT_APPLICABLE,
            "date_discharged": get_utcnow_as_date(),
        }
        self.assertFormValidatorError(
            field="date_discharged",
            expected_msg="This field is not required",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        cleaned_data.update({"date_discharged": None})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_date_discharged_after_date_admitted_ok(self):
        cleaned_data = {
            "patient_admitted": YES,
            "date_admitted": get_utcnow_as_date() - relativedelta(days=1),
            "inpatient_status": DISCHARGED,
            "date_discharged": get_utcnow_as_date(),
        }
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_date_discharged_on_date_admitted_ok(self):
        cleaned_data = {
            "patient_admitted": YES,
            "date_admitted": get_utcnow_as_date(),
            "inpatient_status": DISCHARGED,
            "date_discharged": get_utcnow_as_date(),
        }
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_date_discharged_before_date_admitted_raises_error(self):
        cleaned_data = {
            "patient_admitted": YES,
            "date_admitted": get_utcnow_as_date(),
            "inpatient_status": DISCHARGED,
            "date_discharged": get_utcnow_as_date() - relativedelta(days=1),
        }
        self.assertFormValidatorError(
            field="date_discharged",
            expected_msg="Invalid. Date discharged cannot be before date admitted",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_study_relation_not_yes_with_poss_prob_def_related_raises(self):
        for study_drug in self.study_drugs:
            for study_drug_relation_choice in [
                POSSIBLY_RELATED,
                PROBABLY_RELATED,
                DEFINITELY_RELATED,
            ]:
                for study_relation_choice in [NO, UNKNOWN]:
                    with self.subTest(
                        study_drug=study_drug,
                        study_drug_relation_choice=study_drug_relation_choice,
                        study_relation_choice=study_relation_choice,
                    ):
                        cleaned_data = {
                            f"{study_drug}_relation": study_drug_relation_choice,
                            "ae_study_relation_possibility": study_relation_choice,
                        }
                        study_drug_relationship_label = get_display(
                            STUDY_DRUG_RELATIONSHIP, study_drug_relation_choice
                        )
                        self.assertFormValidatorError(
                            field="ae_study_relation_possibility",
                            expected_msg=(
                                f"Invalid. Cannot be '{study_relation_choice.title()}' if "
                                f"'{study_drug_relationship_label}' "
                                f"to study drug: {study_drug.title()}"
                            ),
                            form_validator=self.validate_form_validator(cleaned_data),
                        )

    def test_study_relation_yes_with_poss_prob_def_related_ok(self):
        for study_drug in self.study_drugs:
            for choice in [POSSIBLY_RELATED, PROBABLY_RELATED, DEFINITELY_RELATED]:
                with self.subTest(study_drug=study_drug, choice=choice):
                    cleaned_data = {
                        f"{study_drug}_relation": choice,
                        "ae_study_relation_possibility": YES,
                    }
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data)
                    )

    # As defined in #465, but superseded by #537
    # def test_study_relation_yes_not_valid_if_not_or_unlikely_related(self):
    #     for study_drug in self.study_drugs:
    #         for choice in [NOT_RELATED, UNLIKELY_RELATED]:
    #             with self.subTest(study_drug=study_drug, choice=choice):
    #                 cleaned_data = {
    #                     f"{study_drug}_relation": choice,
    #                     "ae_study_relation_possibility": YES,
    #                 }
    #                 self.assertFormValidatorError(
    #                     field="ae_study_relation_possibility",
    #                     expected_msg="Invalid. Cannot be 'Yes' if "
    #                     f"'{get_display(STUDY_DRUG_RELATIONSHIP, choice)}' "
    #                     f"to study drug: {study_drug.title()}",
    #                     form_validator=self.validate_form_validator(cleaned_data),
    #                 )
    #
    def test_study_relation_no_with_study_drug_not_related_ok(self):
        for study_drug in self.study_drugs:
            with self.subTest(study_drug=study_drug):
                cleaned_data = {
                    f"{study_drug}_relation": NOT_RELATED,
                    "ae_study_relation_possibility": NO,
                }
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_study_relation_no_with_study_drug_unlikely_ok(self):
        for study_drug in self.study_drugs:
            with self.subTest(study_drug=study_drug):
                cleaned_data = {
                    f"{study_drug}_relation": UNLIKELY_RELATED,
                    "ae_study_relation_possibility": NO,
                }
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_study_relation_no_with_poss_prob_def_related_raises(self):
        choices_subset = [POSSIBLY_RELATED, PROBABLY_RELATED, DEFINITELY_RELATED]
        for study_drug in self.study_drugs:
            for choice in choices_subset:
                with self.subTest(study_drug=study_drug, choice=choice):
                    cleaned_data = {
                        f"{study_drug}_relation": choice,
                        "ae_study_relation_possibility": NO,
                    }
                    self.assertFormValidatorError(
                        field="ae_study_relation_possibility",
                        expected_msg="Invalid. Cannot be 'No' if "
                        f"'{get_display(STUDY_DRUG_RELATIONSHIP, choice)}' "
                        f"to study drug: {study_drug.title()}",
                        form_validator=self.validate_form_validator(cleaned_data),
                    )

    def test_study_relation_unknown_with_poss_prob_def_related_choice_raises(
        self,
    ):
        for study_drug in self.study_drugs:
            for choice in [POSSIBLY_RELATED, PROBABLY_RELATED, DEFINITELY_RELATED]:
                with self.subTest(study_drug=study_drug, choice=choice):
                    cleaned_data = {
                        f"{study_drug}_relation": choice,
                        "ae_study_relation_possibility": UNKNOWN,
                    }
                    self.assertFormValidatorError(
                        field="ae_study_relation_possibility",
                        expected_msg="Invalid. Cannot be 'Unknown' if "
                        f"'{get_display(STUDY_DRUG_RELATIONSHIP, choice)}' "
                        f"to study drug: {study_drug.title()}",
                        form_validator=self.validate_form_validator(cleaned_data),
                    )

    def test_study_relation_unknown_if_not_or_unlikely_related_ok(
        self,
    ):
        choices_subset = [NOT_RELATED, UNLIKELY_RELATED]
        for study_drug in self.study_drugs:
            for choice in choices_subset:
                with self.subTest(study_drug=study_drug, choice=choice):
                    cleaned_data = {
                        f"{study_drug}_relation": choice,
                        "ae_study_relation_possibility": UNKNOWN,
                    }
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data),
                    )

    def test_study_relation_yes_no_unknown_if_not_or_unlikely_related_ok(
        self,
    ):
        for study_drug in self.study_drugs:
            for study_drug_relation_choice in [NOT_RELATED, UNLIKELY_RELATED]:
                for study_relation_choice in [YES, NO, UNKNOWN]:
                    with self.subTest(
                        study_drug=study_drug,
                        study_drug_relation_choice=study_drug_relation_choice,
                        study_relation_choice=study_relation_choice,
                    ):
                        cleaned_data = {
                            f"{study_drug}_relation": study_drug_relation_choice,
                            "ae_study_relation_possibility": study_relation_choice,
                        }
                        self.assertFormValidatorNoError(
                            form_validator=self.validate_form_validator(cleaned_data),
                        )

    def test_flucyt_relation_not_applicable_if_on_control_arm(self):
        self.mock_get_assignment_for_subject.return_value = CONTROL
        self.mock_get_assignment_description_for_subject.return_value = (
            "2 weeks fluconazole alone"
        )
        choices_subset = [
            ch for ch in self.study_drug_relationships_choices if ch != NOT_APPLICABLE
        ]
        for choice in choices_subset:
            with self.subTest(flucyt_relation=choice):
                cleaned_data = {
                    "flucyt_relation": choice,
                    "ae_study_relation_possibility": YES,
                }
                self.assertFormValidatorError(
                    field="flucyt_relation",
                    expected_msg="This field is not applicable. "
                    "Participant is on control arm (2 weeks fluconazole alone).",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

        cleaned_data = {
            "flucyt_relation": NOT_APPLICABLE,
            "ae_study_relation_possibility": YES,
        }
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_flucyt_relation_applicable_if_on_intervention_arm(self):
        self.mock_get_assignment_for_subject.return_value = INTERVENTION
        self.mock_get_assignment_description_for_subject.return_value = (
            "2 weeks fluconazole plus flucytosine"
        )
        cleaned_data = {
            "flucyt_relation": NOT_APPLICABLE,
            "ae_study_relation_possibility": YES,
        }

        self.assertFormValidatorError(
            field="flucyt_relation",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        choices_subset = [
            ch for ch in self.study_drug_relationships_choices if ch != NOT_APPLICABLE
        ]
        for choice in choices_subset:
            with self.subTest(flucyt_relation=choice):
                cleaned_data = {
                    "flucyt_relation": choice,
                    "ae_study_relation_possibility": YES,
                }
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data),
                )
