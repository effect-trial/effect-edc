import arrow
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_adverse_event.choices import STUDY_DRUG_RELATIONSHIP
from edc_constants.constants import NO, NOT_APPLICABLE, UNKNOWN, YES

from effect_ae.choices import INPATIENT_STATUSES
from effect_ae.constants import DEFINITELY_RELATED, DISCHARGED, NOT_RELATED
from effect_ae.form_validators import AeInitialFormValidator
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.followup_form import get_choice_display_text


@tag("aei")
class TestAeInitialFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = AeInitialFormValidator

    inpatient_statuses = [choice[0] for choice in INPATIENT_STATUSES]
    study_drugs = ["fluconazole", "flucytosine"]
    study_drug_relationships_choices = [choice[0] for choice in STUDY_DRUG_RELATIONSHIP]

    @staticmethod
    def get_utcnow_as_date():
        return arrow.utcnow().date()

    def test_date_admitted_required_if_patient_admitted(self):
        cleaned_data = {"patient_admitted": YES, "date_admitted": None}
        self.assertFormValidatorError(
            field="date_admitted",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        cleaned_data.update({"date_admitted": self.get_utcnow_as_date()})
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_date_admitted_not_required_if_patient_not_admitted(self):
        cleaned_data = {
            "patient_admitted": NO,
            "date_admitted": self.get_utcnow_as_date(),
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
            "patient_admitted": YES,
            "date_admitted": self.get_utcnow_as_date(),
            "inpatient_status": NOT_APPLICABLE,
        }
        self.assertFormValidatorError(
            field="inpatient_status",
            expected_msg="This field is applicable",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        for status in [
            value for value in self.inpatient_statuses if value != NOT_APPLICABLE
        ]:
            with self.subTest(status=status):
                cleaned_data.update(
                    {
                        "inpatient_status": status,
                        "date_discharged": self.get_utcnow_as_date()
                        if status == DISCHARGED
                        else None,
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_inpatient_status_not_applicable_if_patient_not_admitted(self):
        for status in [
            value for value in self.inpatient_statuses if value != NOT_APPLICABLE
        ]:
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

    def test_date_discharged_required_if_patient_discharged(self):
        cleaned_data = {
            "patient_admitted": YES,
            "date_admitted": self.get_utcnow_as_date(),
            "inpatient_status": DISCHARGED,
            "date_discharged": None,
        }
        self.assertFormValidatorError(
            field="date_discharged",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        cleaned_data.update({"date_discharged": self.get_utcnow_as_date()})
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
                    "patient_admitted": YES,
                    "date_admitted": self.get_utcnow_as_date(),
                    "inpatient_status": status,
                    "date_discharged": self.get_utcnow_as_date(),
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
            "date_discharged": self.get_utcnow_as_date(),
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
            "date_admitted": self.get_utcnow_as_date() - relativedelta(days=1),
            "inpatient_status": DISCHARGED,
            "date_discharged": self.get_utcnow_as_date(),
        }
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_date_discharged_on_date_admitted_ok(self):
        cleaned_data = {
            "patient_admitted": YES,
            "date_admitted": self.get_utcnow_as_date(),
            "inpatient_status": DISCHARGED,
            "date_discharged": self.get_utcnow_as_date(),
        }
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_date_discharged_before_date_admitted_raises_error(self):
        cleaned_data = {
            "patient_admitted": YES,
            "date_admitted": self.get_utcnow_as_date(),
            "inpatient_status": DISCHARGED,
            "date_discharged": self.get_utcnow_as_date() - relativedelta(days=1),
        }
        self.assertFormValidatorError(
            field="date_discharged",
            expected_msg="Invalid. Date discharged cannot be before date admitted",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_study_relation_yes_valid_with_all_study_drug_choices(self):
        for study_drug in self.study_drugs:
            for choice in self.study_drug_relationships_choices:
                with self.subTest(study_drug=study_drug, choice=choice):
                    cleaned_data = {
                        "ae_study_relation_possibility": YES,
                        f"{study_drug}_relation": choice,
                    }
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data)
                    )

    def test_study_relation_no_valid_with_study_drug_not_related(self):
        for study_drug in self.study_drugs:
            with self.subTest(study_drug=study_drug):
                cleaned_data = {
                    "ae_study_relation_possibility": NO,
                    f"{study_drug}_relation": NOT_RELATED,
                }
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_study_relation_no_invalid_with_study_drug_relation_not_ruled_out(self):
        choices_subset = [
            value
            for value in self.study_drug_relationships_choices
            if value != NOT_RELATED and value != NOT_APPLICABLE
        ]
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
                        f"'{get_choice_display_text(STUDY_DRUG_RELATIONSHIP, choice)}' "
                        f"to study drug: {study_drug.title()}",
                        form_validator=self.validate_form_validator(cleaned_data),
                    )

    def test_study_relation_unknown_invalid_with_definite_study_drug_relation_choice(
        self,
    ):
        for study_drug in self.study_drugs:
            with self.subTest(study_drug=study_drug):
                cleaned_data = {
                    f"{study_drug}_relation": DEFINITELY_RELATED,
                    "ae_study_relation_possibility": UNKNOWN,
                }
                self.assertFormValidatorError(
                    field="ae_study_relation_possibility",
                    expected_msg="Invalid. Cannot be 'Unknown' if 'Definitely related' "
                    f"to study drug: {study_drug.title()}",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_study_relation_unknown_valid_with_non_definite_study_drug_relation_choices(
        self,
    ):
        choices_subset = [
            value
            for value in self.study_drug_relationships_choices
            if value != DEFINITELY_RELATED
        ]
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
