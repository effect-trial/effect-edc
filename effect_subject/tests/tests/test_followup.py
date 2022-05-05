from copy import deepcopy
from dataclasses import dataclass

from django.test import TestCase, tag
from edc_constants.constants import (
    COLLATERAL_HISTORY,
    DEAD,
    HOSPITAL_NOTES,
    IN_PERSON,
    NEXT_OF_KIN,
    NO,
    NOT_APPLICABLE,
    OTHER,
    OUTPATIENT_CARDS,
    PATIENT,
    TELEPHONE,
    YES,
)
from edc_visit_tracking.choices import ASSESSMENT_WHO_CHOICES, VISIT_INFO_SOURCE2

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.choices import PATIENT_STATUSES
from effect_subject.forms.followup_form import FollowupFormValidator
from effect_visit_schedule.constants import DAY01, DAY14


@tag("fu")
class TestFollowupFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = FollowupFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()
        self.subject_visit.appointment.visit_code = DAY14

    def get_valid_in_person_visit_data(self):
        self.subject_visit.info_source = PATIENT
        return {
            "subject_visit": self.subject_visit,
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "assessment_type": IN_PERSON,
            "assessment_type_other": "",
            "info_source": NOT_APPLICABLE,
            "info_source_other": "",
            "survival_status": "alive_well",
            "hospitalized": NO,
            "adherence_counselling": YES,
        }

    def get_valid_patient_telephone_assessment_data(self):
        self.subject_visit.info_source = PATIENT
        return {
            "subject_visit": self.subject_visit,
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "assessment_type": TELEPHONE,
            "assessment_type_other": "",
            "info_source": PATIENT,
            "info_source_other": "",
            "survival_status": "alive_well",
            "hospitalized": YES,
            "adherence_counselling": YES,
        }

    def get_valid_next_of_kin_telephone_assessment_data(self):
        cleaned_data = deepcopy(self.get_valid_patient_telephone_assessment_data())
        self.subject_visit.info_source = COLLATERAL_HISTORY
        cleaned_data.update(
            {
                "subject_visit": self.subject_visit,
                "info_source": NEXT_OF_KIN,
            }
        )
        return cleaned_data

    def get_valid_other_assessment_type_data(self):
        cleaned_data = deepcopy(self.get_valid_in_person_visit_data())
        self.subject_visit.info_source = HOSPITAL_NOTES
        cleaned_data.update(
            {
                "subject_visit": self.subject_visit,
                "assessment_type": OTHER,
                "assessment_type_other": "Some other assessment type",
            }
        )
        return cleaned_data

    def test_form_validator_allows_valid_in_person_visit(self):
        cleaned_data = self.get_valid_in_person_visit_data()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_form_validator_allows_valid_patient_telephone_assessment(self):
        cleaned_data = self.get_valid_patient_telephone_assessment_data()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_form_validator_allows_valid_nok_telephone_assessment(self):
        cleaned_data = self.get_valid_next_of_kin_telephone_assessment_data()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_form_validator_allows_valid_other_assessment_type(self):
        cleaned_data = self.get_valid_other_assessment_type_data()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_form_validator_denies_patient_telephone_assessment_at_baseline(self):
        cleaned_data = self.get_valid_patient_telephone_assessment_data()
        self.subject_visit.appointment.visit_code = DAY01
        cleaned_data.update({"subject_visit": self.subject_visit})
        self.assertFormValidatorError(
            field="assessment_type",
            expected_msg="Invalid. Expected 'In person' at baseline",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_assessment_type_other_required_if_specified(self):
        cleaned_data = self.get_valid_other_assessment_type_data()
        cleaned_data.update({"assessment_type_other": ""})
        self.assertFormValidatorError(
            field="assessment_type_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"assessment_type_other": "Some other assessment type"})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_assessment_type_other_not_required_if_not_specified(self):
        cleaned_data = self.get_valid_in_person_visit_data()
        cleaned_data.update(
            {
                "assessment_type": IN_PERSON,
                "assessment_type_other": "Some other assessment type",
            }
        )
        self.assertFormValidatorError(
            field="assessment_type_other",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"assessment_type_other": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_info_source_na_for_in_person_visit(self):
        cleaned_data = self.get_valid_in_person_visit_data()
        cleaned_data.update({"info_source": PATIENT})
        self.assertFormValidatorError(
            field="info_source",
            expected_msg="This field is not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_info_source_na_for_other_assessment_type(self):
        cleaned_data = self.get_valid_other_assessment_type_data()
        cleaned_data.update({"info_source": PATIENT})
        self.assertFormValidatorError(
            field="info_source",
            expected_msg="This field is not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_info_source_applicable_for_telephone_assessments(self):
        cleaned_data = self.get_valid_patient_telephone_assessment_data()
        cleaned_data.update({"info_source": NOT_APPLICABLE})
        self.assertFormValidatorError(
            field="info_source",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_info_source_other_required_if_specified(self):
        cleaned_data = self.get_valid_patient_telephone_assessment_data()
        cleaned_data.update({"info_source": OTHER})
        self.assertFormValidatorError(
            field="info_source_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_info_source_other_not_required_if_not_specified(self):
        cleaned_data = self.get_valid_patient_telephone_assessment_data()
        cleaned_data.update({"info_source_other": "xxx"})
        self.assertFormValidatorError(
            field="info_source_other",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_sv_info_source_raises_error_if_does_not_reconcile_with_patient_followup_answers(
        self,
    ):
        for sv_info_source in [src[0] for src in VISIT_INFO_SOURCE2 if src[0] != PATIENT]:
            with self.subTest(sv_info_source=sv_info_source):
                cleaned_data = self.get_valid_in_person_visit_data()
                self.subject_visit.info_source = sv_info_source
                cleaned_data.update({"subject_visit": self.subject_visit})

                expected_msg = FollowupFormValidator.get_sv_info_source_mismatch_error_msg(
                    sv_info_source=sv_info_source,
                    fu_assessment_type=cleaned_data.get("assessment_type"),
                    fu_info_source=cleaned_data.get("info_source"),
                )
                self.assertFormValidatorError(
                    field="assessment_type",
                    expected_msg=expected_msg,
                    form_validator=self.validate_form_validator(cleaned_data),
                    expected_errors=2,
                )
                self.assertFormValidatorError(
                    field="info_source",
                    expected_msg=expected_msg,
                    form_validator=self.validate_form_validator(cleaned_data),
                    expected_errors=2,
                )

    def test_sv_info_source_raises_error_if_does_not_reconcile_with_nok_telephone_answers(
        self,
    ):
        for sv_info_source in [
            src[0] for src in VISIT_INFO_SOURCE2 if src[0] != COLLATERAL_HISTORY
        ]:
            with self.subTest(sv_info_source=sv_info_source):
                cleaned_data = self.get_valid_next_of_kin_telephone_assessment_data()
                self.subject_visit.info_source = sv_info_source
                cleaned_data.update({"subject_visit": self.subject_visit})

                expected_msg = FollowupFormValidator.get_sv_info_source_mismatch_error_msg(
                    sv_info_source=sv_info_source,
                    fu_assessment_type=cleaned_data.get("assessment_type"),
                    fu_info_source=cleaned_data.get("info_source"),
                )
                self.assertFormValidatorError(
                    field="assessment_type",
                    expected_msg=expected_msg,
                    form_validator=self.validate_form_validator(cleaned_data),
                    expected_errors=2,
                )
                self.assertFormValidatorError(
                    field="info_source",
                    expected_msg=expected_msg,
                    form_validator=self.validate_form_validator(cleaned_data),
                    expected_errors=2,
                )

    def test_sv_info_source_raises_error_if_does_not_reconcile_with_other_assessment_type(
        self,
    ):
        for sv_info_source in [
            src[0]
            for src in VISIT_INFO_SOURCE2
            if src[0] not in [COLLATERAL_HISTORY, HOSPITAL_NOTES, OUTPATIENT_CARDS, OTHER]
        ]:
            with self.subTest(sv_info_source=sv_info_source):
                cleaned_data = self.get_valid_other_assessment_type_data()
                self.subject_visit.info_source = sv_info_source
                cleaned_data.update({"subject_visit": self.subject_visit})

                expected_msg = FollowupFormValidator.get_sv_info_source_mismatch_error_msg(
                    sv_info_source=sv_info_source,
                    fu_assessment_type=cleaned_data.get("assessment_type"),
                    fu_info_source=cleaned_data.get("info_source"),
                )
                self.assertFormValidatorError(
                    field="assessment_type",
                    expected_msg=expected_msg,
                    form_validator=self.validate_form_validator(cleaned_data),
                    expected_errors=2,
                )
                self.assertFormValidatorError(
                    field="info_source",
                    expected_msg=expected_msg,
                    form_validator=self.validate_form_validator(cleaned_data),
                    expected_errors=2,
                )

    def test_deceased_status_invalid_at_baseline(self):
        cleaned_data = self.get_valid_other_assessment_type_data()
        self.subject_visit.appointment.visit_code = DAY01
        cleaned_data.update(
            {
                "subject_visit": self.subject_visit,
                "survival_status": DEAD,
            }
        )
        self.assertFormValidatorError(
            field="survival_status",
            expected_msg="Invalid: Cannot be 'Deceased' at baseline",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_deceased_status_invalid_for_in_person_visit(self):
        cleaned_data = self.get_valid_in_person_visit_data()
        cleaned_data.update({"survival_status": DEAD})
        self.assertFormValidatorError(
            field="survival_status",
            expected_msg="Invalid: Cannot be 'Deceased' if this is an 'In person' visit",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_deceased_status_invalid_for_patient_telephone_visit(self):
        cleaned_data = self.get_valid_patient_telephone_assessment_data()
        cleaned_data.update({"survival_status": DEAD})
        self.assertFormValidatorError(
            field="survival_status",
            expected_msg=(
                "Invalid: Unexpected survival status 'Deceased' if "
                "'Telephone' visit with 'Patient'"
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_deceased_status_valid_for_other_telephone_visits(self):
        info_sources = [
            src[0] for src in ASSESSMENT_WHO_CHOICES if src[0] not in [PATIENT, NOT_APPLICABLE]
        ]
        for info_src in info_sources:
            with self.subTest(info_src=info_src):
                cleaned_data = deepcopy(self.get_valid_next_of_kin_telephone_assessment_data())
                cleaned_data.update(
                    {
                        "info_source": info_src,
                        "info_source_other": "xxx" if info_src == OTHER else "",
                        "survival_status": DEAD,
                        "adherence_counselling": NOT_APPLICABLE,
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_hospitalized_yes_invalid_at_baseline(self):
        cleaned_data = self.get_valid_in_person_visit_data()
        self.subject_visit.appointment.visit_code = DAY01
        cleaned_data.update(
            {
                "subject_visit": self.subject_visit,
                "hospitalized": YES,
            }
        )
        self.assertFormValidatorError(
            field="hospitalized",
            expected_msg="Invalid. Expected NO at baseline",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_adherence_counselling_na_if_deceased(self):
        cleaned_data = self.get_valid_next_of_kin_telephone_assessment_data()
        cleaned_data.update({"survival_status": DEAD})
        self.assertFormValidatorError(
            field="adherence_counselling",
            expected_msg="Invalid: Expected 'Not applicable' if survival status is 'Deceased'",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_adherence_counselling_applicable_if_not_deceased(self):
        survival_statuses = [ss[0] for ss in PATIENT_STATUSES if ss[0] != DEAD]
        for survival_status in survival_statuses:
            with self.subTest(survival_status=survival_status):
                cleaned_data = deepcopy(self.get_valid_next_of_kin_telephone_assessment_data())
                cleaned_data.update(
                    {
                        "survival_status": survival_status,
                        "adherence_counselling": NOT_APPLICABLE,
                    }
                )
                self.assertFormValidatorError(
                    field="adherence_counselling",
                    expected_msg="This field is applicable.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )


@dataclass
class SvFuChoices:
    sv_info_source: str
    fu_assessment_type: str
    fu_info_source: str


class TestSubjectVisitFollowupValidationLogic(TestCase):
    def test_returns_true_for_valid_choice_combos(self):
        valid_combos = (
            # Valid combos when subject visit info source is 'Patient'
            SvFuChoices(
                sv_info_source=PATIENT,
                fu_assessment_type=IN_PERSON,
                fu_info_source=NOT_APPLICABLE,
            ),
            SvFuChoices(
                sv_info_source=PATIENT,
                fu_assessment_type=TELEPHONE,
                fu_info_source=PATIENT,
            ),
            # Valid combos when subject visit info source is 'Collateral History'
            SvFuChoices(
                sv_info_source=COLLATERAL_HISTORY,
                fu_assessment_type=TELEPHONE,
                fu_info_source=NEXT_OF_KIN,
            ),
            SvFuChoices(
                sv_info_source=COLLATERAL_HISTORY,
                fu_assessment_type=TELEPHONE,
                fu_info_source=OTHER,
            ),
            SvFuChoices(
                sv_info_source=COLLATERAL_HISTORY,
                fu_assessment_type=OTHER,
                fu_info_source=NOT_APPLICABLE,
            ),
            # Valid combos when subject visit info source is 'Hospital notes',
            # 'Outpatient cards', or 'Other'
            SvFuChoices(
                sv_info_source=HOSPITAL_NOTES,
                fu_assessment_type=OTHER,
                fu_info_source=NOT_APPLICABLE,
            ),
            SvFuChoices(
                sv_info_source=OUTPATIENT_CARDS,
                fu_assessment_type=OTHER,
                fu_info_source=NOT_APPLICABLE,
            ),
            SvFuChoices(
                sv_info_source=OTHER,
                fu_assessment_type=OTHER,
                fu_info_source=NOT_APPLICABLE,
            ),
        )
        for combo in valid_combos:
            with self.subTest(combo=combo):
                self.assertTrue(
                    FollowupFormValidator.sv_info_source_reconciles_with_fu(
                        sv_info_source=combo.sv_info_source,
                        fu_assessment_type=combo.fu_assessment_type,
                        fu_info_source=combo.fu_info_source,
                    )
                )

    def test_returns_false_for_invalid_choice_combos(self):
        invalid_combos = (
            # Invalid combos when subject visit info source is 'Patient'
            SvFuChoices(
                sv_info_source=PATIENT,
                fu_assessment_type=TELEPHONE,
                fu_info_source=NEXT_OF_KIN,
            ),
            SvFuChoices(
                sv_info_source=PATIENT,
                fu_assessment_type=TELEPHONE,
                fu_info_source=OTHER,
            ),
            SvFuChoices(
                sv_info_source=PATIENT,
                fu_assessment_type=TELEPHONE,
                fu_info_source=NOT_APPLICABLE,
            ),
            SvFuChoices(
                sv_info_source=PATIENT,
                fu_assessment_type=OTHER,
                fu_info_source=IN_PERSON,
            ),
            SvFuChoices(
                sv_info_source=PATIENT,
                fu_assessment_type=OTHER,
                fu_info_source=NEXT_OF_KIN,
            ),
            SvFuChoices(
                sv_info_source=PATIENT,
                fu_assessment_type=OTHER,
                fu_info_source=NOT_APPLICABLE,
            ),
            # Invalid combos when subject visit info source is 'Collateral History'
            SvFuChoices(
                sv_info_source=COLLATERAL_HISTORY,
                fu_assessment_type=IN_PERSON,
                fu_info_source=NOT_APPLICABLE,
            ),
            SvFuChoices(
                sv_info_source=COLLATERAL_HISTORY,
                fu_assessment_type=TELEPHONE,
                fu_info_source=PATIENT,
            ),
            SvFuChoices(
                sv_info_source=COLLATERAL_HISTORY,
                fu_assessment_type=TELEPHONE,
                fu_info_source=NOT_APPLICABLE,
            ),
            # Invalid combos when subject visit info source is 'Hospital notes',
            # 'Outpatient cards', or 'Other'
            SvFuChoices(
                sv_info_source=HOSPITAL_NOTES,
                fu_assessment_type=IN_PERSON,
                fu_info_source=NOT_APPLICABLE,
            ),
            SvFuChoices(
                sv_info_source=OUTPATIENT_CARDS,
                fu_assessment_type=IN_PERSON,
                fu_info_source=NOT_APPLICABLE,
            ),
            SvFuChoices(
                sv_info_source=OTHER,
                fu_assessment_type=IN_PERSON,
                fu_info_source=NOT_APPLICABLE,
            ),
            SvFuChoices(
                sv_info_source=HOSPITAL_NOTES,
                fu_assessment_type=TELEPHONE,
                fu_info_source=PATIENT,
            ),
            SvFuChoices(
                sv_info_source=OUTPATIENT_CARDS,
                fu_assessment_type=TELEPHONE,
                fu_info_source=PATIENT,
            ),
            SvFuChoices(
                sv_info_source=OTHER,
                fu_assessment_type=TELEPHONE,
                fu_info_source=PATIENT,
            ),
            SvFuChoices(
                sv_info_source=HOSPITAL_NOTES,
                fu_assessment_type=TELEPHONE,
                fu_info_source=NEXT_OF_KIN,
            ),
            SvFuChoices(
                sv_info_source=OUTPATIENT_CARDS,
                fu_assessment_type=TELEPHONE,
                fu_info_source=NEXT_OF_KIN,
            ),
            SvFuChoices(
                sv_info_source=OTHER,
                fu_assessment_type=TELEPHONE,
                fu_info_source=NEXT_OF_KIN,
            ),
            SvFuChoices(
                sv_info_source=HOSPITAL_NOTES,
                fu_assessment_type=TELEPHONE,
                fu_info_source=OTHER,
            ),
            SvFuChoices(
                sv_info_source=OUTPATIENT_CARDS,
                fu_assessment_type=TELEPHONE,
                fu_info_source=OTHER,
            ),
            SvFuChoices(
                sv_info_source=OTHER,
                fu_assessment_type=TELEPHONE,
                fu_info_source=OTHER,
            ),
            # Invalid combos when subject visit info source is 'Not applicable (if missed)'
            SvFuChoices(
                sv_info_source=NOT_APPLICABLE,
                fu_assessment_type=IN_PERSON,
                fu_info_source=PATIENT,
            ),
            SvFuChoices(
                sv_info_source=NOT_APPLICABLE,
                fu_assessment_type=TELEPHONE,
                fu_info_source=PATIENT,
            ),
            SvFuChoices(
                sv_info_source=NOT_APPLICABLE,
                fu_assessment_type=TELEPHONE,
                fu_info_source=NEXT_OF_KIN,
            ),
        )
        for combo in invalid_combos:
            with self.subTest(combo=combo):
                self.assertFalse(
                    FollowupFormValidator.sv_info_source_reconciles_with_fu(
                        sv_info_source=combo.sv_info_source,
                        fu_assessment_type=combo.fu_assessment_type,
                        fu_info_source=combo.fu_info_source,
                    )
                )
