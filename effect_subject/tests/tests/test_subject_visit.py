from copy import deepcopy

from django.test import TestCase, tag
from edc_constants.constants import ALIVE, DEAD, NO, NOT_APPLICABLE, OTHER, YES
from edc_visit_schedule.constants import DAY1, DAY3
from edc_visit_tracking.constants import SCHEDULED

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.choices import ASSESSMENT_WHO_CHOICES
from effect_subject.constants import IN_PERSON, NEXT_OF_KIN, PATIENT, TELEPHONE
from effect_subject.forms.subject_visit_form import SubjectVisitFormValidator
from effect_visit_schedule.constants import DAY14
from effect_visit_schedule.visit_schedules.schedule import visits


@tag("sv")
class TestSubjectVisitFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = SubjectVisitFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()
        self.subject_visit_codes = [v.code for v in visits if v.code <= DAY14]

    def set_subject_visit(self, visit_code: str):
        for vc in sorted(self.subject_visit_codes):
            if vc == visit_code:
                break
            self.subject_visit = self.get_next_subject_visit(self.subject_visit)

    def get_valid_in_person_sv_data(self, visit_code: str = DAY1):
        self.set_subject_visit(visit_code=visit_code)
        return {
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "reason": SCHEDULED,
            "reason_unscheduled": NOT_APPLICABLE,
            "reason_unscheduled_other": "",
            "assessment_type": IN_PERSON,
            "assessment_type_other": "",
            "assessment_who": PATIENT,
            "assessment_who_other": "",
            "info_source": PATIENT,
            "info_source_other": "",
            "survival_status": ALIVE,
            "last_alive_date": "",
            "hospitalized": NO,
            "comments": "",
        }

    def get_valid_patient_telephone_sv_data(self, visit_code: str = DAY3):
        cleaned_data = deepcopy(self.get_valid_in_person_sv_data(visit_code))
        cleaned_data.update({"assessment_type": TELEPHONE})
        return cleaned_data

    def get_valid_nok_sv_data(self, visit_code: str = DAY3):
        cleaned_data = deepcopy(self.get_valid_in_person_sv_data(visit_code))
        cleaned_data.update(
            {
                "assessment_type": TELEPHONE,
                "assessment_who": NEXT_OF_KIN,
            }
        )
        return cleaned_data

    def get_valid_assessment_type_other_sv_data(self, visit_code: str = DAY3):
        cleaned_data = deepcopy(self.get_valid_in_person_sv_data(visit_code))
        cleaned_data.update(
            {
                "assessment_type": OTHER,
                "assessment_type_other": "Some other assessment type",
            }
        )
        return cleaned_data

    def get_valid_assessment_who_other_sv_data(self, visit_code: str = DAY3):
        cleaned_data = deepcopy(self.get_valid_in_person_sv_data(visit_code))
        cleaned_data.update(
            {
                "assessment_type": TELEPHONE,
                "assessment_type_other": "",
                "assessment_who": OTHER,
                "assessment_who_other": "Some other entity",
            }
        )
        return cleaned_data

    def test_valid_in_person_sv_data_ok(self):
        cleaned_data = self.get_valid_in_person_sv_data(visit_code=DAY1)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_patient_telephone_sv_data_ok(self):
        cleaned_data = self.get_valid_patient_telephone_sv_data(visit_code=DAY3)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_nok_sv_data_ok(self):
        cleaned_data = self.get_valid_nok_sv_data(visit_code=DAY3)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_assessment_type_other_sv_data_ok(self):
        cleaned_data = self.get_valid_assessment_type_other_sv_data(visit_code=DAY3)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_assessment_type_who_sv_data_ok(self):
        cleaned_data = self.get_valid_assessment_who_other_sv_data(visit_code=DAY3)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_baseline_must_be_in_person(self):
        cleaned_data = self.get_valid_in_person_sv_data()
        cleaned_data.update({"assessment_type": TELEPHONE})
        self.assertFormValidatorError(
            field="assessment_type",
            expected_msg="Invalid. Expected 'In person' at baseline",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "assessment_type": OTHER,
                "assessment_type_other": "Some other assessment type",
            }
        )
        self.assertFormValidatorError(
            field="assessment_type",
            expected_msg="Invalid. Expected 'In person' at baseline",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_after_baseline_can_be_any_assessment_type(self):
        for visit_code in [vc for vc in self.subject_visit_codes if vc != DAY1]:
            with self.subTest(visit_code=visit_code):
                cleaned_data = self.get_valid_in_person_sv_data(visit_code=visit_code)
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

                cleaned_data.update({"assessment_type": TELEPHONE})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

                cleaned_data.update(
                    {
                        "assessment_type": OTHER,
                        "assessment_type_other": "Some other assessment type",
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_assessment_type_other_required_if_specified(self):
        cleaned_data = self.get_valid_assessment_type_other_sv_data(visit_code=DAY3)
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
        cleaned_data = self.get_valid_assessment_type_other_sv_data(visit_code=DAY3)
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

    def test_assessment_who_other_required_if_specified(self):
        cleaned_data = self.get_valid_assessment_who_other_sv_data(visit_code=DAY3)
        cleaned_data.update({"assessment_who_other": ""})
        self.assertFormValidatorError(
            field="assessment_who_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"assessment_who_other": "Some other entity"})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_assessment_type_who_other_not_required_if_not_specified(self):
        cleaned_data = self.get_valid_assessment_who_other_sv_data(visit_code=DAY3)
        cleaned_data.update(
            {
                "assessment_who": PATIENT,
                "assessment_who_other": "Some other entity",
            }
        )
        self.assertFormValidatorError(
            field="assessment_who_other",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"assessment_who_other": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_deceased_status_invalid_at_baseline(self):
        cleaned_data = self.get_valid_in_person_sv_data(visit_code=DAY1)
        cleaned_data.update({"survival_status": DEAD})
        self.assertFormValidatorError(
            field="survival_status",
            expected_msg="Invalid: Cannot be 'Deceased' at baseline",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_deceased_status_invalid_for_in_person_visit(self):
        cleaned_data = self.get_valid_in_person_sv_data(visit_code=DAY14)
        cleaned_data.update({"survival_status": DEAD})
        self.assertFormValidatorError(
            field="survival_status",
            expected_msg="Invalid: Expected 'Alive' if this is an 'In person' visit",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_deceased_status_invalid_for_patient_telephone_visit(self):
        cleaned_data = self.get_valid_patient_telephone_sv_data(visit_code=DAY3)
        cleaned_data.update({"survival_status": DEAD})
        self.assertFormValidatorError(
            field="survival_status",
            expected_msg="Invalid: Expected 'Alive' if spoke to 'Patient'",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_deceased_status_valid_for_other_telephone_visits(self):
        sources = [src[0] for src in ASSESSMENT_WHO_CHOICES if src[0] not in [PATIENT]]
        for assessment_who in sources:
            with self.subTest(assessment_who=assessment_who):
                cleaned_data = deepcopy(self.get_valid_nok_sv_data(visit_code=DAY3))
                cleaned_data.update(
                    {
                        "assessment_who": assessment_who,
                        "assessment_who_other": "xxx"
                        if assessment_who == OTHER
                        else "",
                        "survival_status": DEAD,
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_hospitalized_yes_invalid_at_baseline(self):
        cleaned_data = self.get_valid_in_person_sv_data(visit_code=DAY1)
        cleaned_data.update({"hospitalized": YES})
        self.assertFormValidatorError(
            field="hospitalized",
            expected_msg="Invalid. Expected NO at baseline",
            form_validator=self.validate_form_validator(cleaned_data),
        )
