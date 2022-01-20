from copy import deepcopy

from django.test import TestCase
from edc_constants.constants import DEAD, NO, NOT_APPLICABLE, OTHER, YES
from model_bakery import baker

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.choices import INFO_SOURCES, PATIENT_STATUSES
from effect_subject.constants import IN_PERSON, PATIENT, TELEPHONE
from effect_subject.forms import FollowupForm
from effect_subject.forms.followup_form import FollowupFormValidator


class TestFollowup(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def test_ok(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)
        obj = baker.make_recipe("effect_subject.followup", subject_visit=subject_visit)
        form = FollowupForm(instance=obj)
        form.is_valid()


class TestFollowupFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = FollowupFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_valid_in_person_visit_data(self):
        return {
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "assessment_type": IN_PERSON,
            "info_source": NOT_APPLICABLE,
            "info_source_other": "",
            "survival_status": "alive_well",
            "hospitalized": NO,
            "adherence_counselling": YES,
        }

    def get_valid_patient_telephone_assessment_data(self):
        return {
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "assessment_type": TELEPHONE,
            "info_source": PATIENT,
            "info_source_other": "",
            "survival_status": "alive_well",
            "hospitalized": YES,
            "adherence_counselling": YES,
        }

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
        cleaned_data = self.get_valid_patient_telephone_assessment_data()
        cleaned_data.update({"info_source": "next_of_kin"})
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

    def test_deceased_status_invalid_for_in_person_visit(self):
        cleaned_data = self.get_valid_in_person_visit_data()
        cleaned_data.update({"survival_status": DEAD})
        self.assertFormValidatorError(
            field="survival_status",
            expected_msg="Invalid: Unexpected survival status 'Deceased' if 'In person' visit",
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
            src[0] for src in INFO_SOURCES if src[0] not in [PATIENT, NOT_APPLICABLE]
        ]
        for info_src in info_sources:
            with self.subTest(info_src=info_src):
                cleaned_data = deepcopy(
                    self.get_valid_patient_telephone_assessment_data()
                )
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

    def test_adherence_counselling_na_if_deceased(self):
        cleaned_data = self.get_valid_patient_telephone_assessment_data()
        cleaned_data.update({"info_source": "next_of_kin", "survival_status": DEAD})
        self.assertFormValidatorError(
            field="adherence_counselling",
            expected_msg="Invalid: Expected 'Not applicable' if survival status is 'Deceased'",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_adherence_counselling_applicable_if_not_deceased(self):
        survival_statuses = [ss[0] for ss in PATIENT_STATUSES if ss[0] != DEAD]
        for survival_status in survival_statuses:
            with self.subTest(survival_status=survival_status):
                cleaned_data = deepcopy(
                    self.get_valid_patient_telephone_assessment_data()
                )
                cleaned_data.update(
                    {
                        "info_source": "next_of_kin",
                        "survival_status": survival_status,
                        "adherence_counselling": NOT_APPLICABLE,
                    }
                )
                self.assertFormValidatorError(
                    field="adherence_counselling",
                    expected_msg="This field is applicable.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )
