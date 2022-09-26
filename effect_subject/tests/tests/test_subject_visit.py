from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

from django.test import TestCase
from edc_constants.constants import (
    ALIVE,
    DEAD,
    HOSPITAL_NOTES,
    IN_PERSON,
    NEXT_OF_KIN,
    NO,
    NOT_APPLICABLE,
    OTHER,
    OUTPATIENT_CARDS,
    PATIENT,
    PATIENT_REPRESENTATIVE,
    TELEPHONE,
    UNKNOWN,
    YES,
)
from edc_visit_tracking.choices import ASSESSMENT_WHO_CHOICES, VISIT_INFO_SOURCE2
from edc_visit_tracking.constants import SCHEDULED

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.subject_visit_form import SubjectVisitFormValidator
from effect_subject.models import SubjectVisit
from effect_visit_schedule.constants import DAY01, DAY03, DAY14


class TestSubjectVisitFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_cls = SubjectVisitFormValidator
    form_validator_model_cls = SubjectVisit

    def setUp(self) -> None:
        super().setUp()
        subject_visit = self.get_subject_visit()
        subject_visit = self.get_next_subject_visit(subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.get_next_subject_visit(subject_visit)

    @staticmethod
    def get_valid_in_person_sv_data(visit_code: Optional[str] = None):
        visit_code = visit_code or DAY01
        subject_visit = SubjectVisit.objects.get(visit_code=visit_code)
        return {
            "appointment": subject_visit.appointment,
            "report_datetime": subject_visit.report_datetime,
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

    def get_valid_patient_telephone_sv_data(self, visit_code: Optional[str] = None):
        visit_code = visit_code or DAY03
        cleaned_data = deepcopy(self.get_valid_in_person_sv_data(visit_code))
        cleaned_data.update({"assessment_type": TELEPHONE})
        return cleaned_data

    def get_valid_nok_sv_data(self, visit_code: Optional[str] = None):
        visit_code = visit_code or DAY03
        cleaned_data = deepcopy(self.get_valid_in_person_sv_data(visit_code))
        cleaned_data.update(
            {
                "assessment_type": TELEPHONE,
                "assessment_who": NEXT_OF_KIN,
                "info_source": PATIENT_REPRESENTATIVE,
            }
        )
        return cleaned_data

    def get_valid_assessment_type_other_sv_data(self, visit_code: Optional[str] = None):
        visit_code = visit_code or DAY03
        cleaned_data = deepcopy(self.get_valid_in_person_sv_data(visit_code))
        cleaned_data.update(
            {
                "assessment_type": OTHER,
                "assessment_type_other": "Some other assessment type",
                "info_source": OUTPATIENT_CARDS,
            }
        )
        return cleaned_data

    def get_valid_assessment_who_other_sv_data(self, visit_code: Optional[str] = None):
        visit_code = visit_code or DAY03
        cleaned_data = deepcopy(self.get_valid_in_person_sv_data(visit_code))
        cleaned_data.update(
            {
                "assessment_type": TELEPHONE,
                "assessment_type_other": "",
                "assessment_who": OTHER,
                "assessment_who_other": "Some other entity",
                "info_source": HOSPITAL_NOTES,
            }
        )
        return cleaned_data

    def test_valid_in_person_sv_data_ok(self):
        cleaned_data = self.get_valid_in_person_sv_data(visit_code=DAY01)
        form_validator = SubjectVisitFormValidator(
            cleaned_data=cleaned_data, instance=SubjectVisit()
        )
        form_validator.validate()

    def test_valid_patient_telephone_sv_data_ok(self):
        cleaned_data = self.get_valid_patient_telephone_sv_data(visit_code=DAY03)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit())
        )

    def test_valid_nok_sv_data_ok(self):
        cleaned_data = self.get_valid_nok_sv_data(visit_code=DAY03)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit())
        )

    def test_valid_assessment_type_other_sv_data_ok(self):
        cleaned_data = self.get_valid_assessment_type_other_sv_data(visit_code=DAY03)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit())
        )

    def test_valid_assessment_who_other_sv_data_ok(self):
        cleaned_data = self.get_valid_assessment_who_other_sv_data(visit_code=DAY03)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit())
        )

    def test_baseline_must_be_in_person(self):
        cleaned_data = self.get_valid_in_person_sv_data(visit_code=DAY01)
        cleaned_data.update({"assessment_type": TELEPHONE})
        self.assertFormValidatorError(
            field="assessment_type",
            expected_msg="Invalid. Expected 'In person' at baseline",
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
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
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

    def test_after_baseline_can_be_any_assessment_type(self):
        for subject_visit in SubjectVisit.objects.exclude(visit_code=DAY01).order_by(
            "visit_code"
        ):
            with self.subTest(visit_code=subject_visit.visit_code):
                cleaned_data = self.get_valid_in_person_sv_data(
                    visit_code=subject_visit.visit_code
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(
                        cleaned_data, instance=SubjectVisit()
                    )
                )

                cleaned_data.update({"assessment_type": TELEPHONE})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(
                        cleaned_data, instance=SubjectVisit()
                    )
                )

                cleaned_data.update(
                    {
                        "assessment_type": OTHER,
                        "assessment_type_other": "Some other assessment type",
                        "info_source": HOSPITAL_NOTES,
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(
                        cleaned_data, instance=SubjectVisit()
                    )
                )

    def test_assessment_type_other_required_if_specified(self):
        cleaned_data = self.get_valid_assessment_type_other_sv_data(visit_code=DAY03)
        cleaned_data.update({"assessment_type_other": ""})
        self.assertFormValidatorError(
            field="assessment_type_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

        cleaned_data.update({"assessment_type_other": "Some other assessment type"})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit())
        )

    def test_assessment_type_other_not_required_if_not_specified(self):
        cleaned_data = self.get_valid_assessment_type_other_sv_data(visit_code=DAY03)
        cleaned_data.update(
            {
                "assessment_type": IN_PERSON,
                "assessment_type_other": "Some other assessment type",
            }
        )
        self.assertFormValidatorError(
            field="assessment_type_other",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

        cleaned_data.update({"assessment_type_other": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit())
        )

    def test_in_person_visit_expects_speak_to_patient(self):
        cleaned_data = self.get_valid_in_person_sv_data()
        cleaned_data.update({"assessment_who": NEXT_OF_KIN})
        self.assertFormValidatorError(
            field="assessment_who",
            expected_msg="Invalid. Expected 'Patient' if 'In person' visit",
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

        cleaned_data.update(
            {
                "assessment_who": OTHER,
                "assessment_who_other": "Some other assessment entity",
            }
        )
        self.assertFormValidatorError(
            field="assessment_who",
            expected_msg="Invalid. Expected 'Patient' if 'In person' visit",
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

        cleaned_data.update(
            {
                "assessment_who": PATIENT,
                "assessment_who_other": "",
            }
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit())
        )

    def test_after_baseline_can_be_any_assessment_who(self):
        for subject_visit in SubjectVisit.objects.exclude(visit_code=DAY01).order_by(
            "visit_code"
        ):
            with self.subTest(visit_code=subject_visit.visit_code):
                cleaned_data = self.get_valid_in_person_sv_data(
                    visit_code=subject_visit.visit_code
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(
                        cleaned_data, instance=SubjectVisit()
                    )
                )

                cleaned_data.update(
                    {
                        "assessment_type": TELEPHONE,
                        "assessment_who": NEXT_OF_KIN,
                        "info_source": PATIENT_REPRESENTATIVE,
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(
                        cleaned_data, instance=SubjectVisit()
                    )
                )

                cleaned_data.update(
                    {
                        "assessment_who": OTHER,
                        "assessment_who_other": "Some other entity",
                        "info_source": OTHER,
                        "info_source_other": "Some other information source",
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(
                        cleaned_data, instance=SubjectVisit()
                    )
                )

    def test_assessment_who_other_required_if_specified(self):
        cleaned_data = self.get_valid_assessment_who_other_sv_data(visit_code=DAY03)
        cleaned_data.update({"assessment_who_other": ""})
        self.assertFormValidatorError(
            field="assessment_who_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

        cleaned_data.update({"assessment_who_other": "Some other entity"})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit())
        )

    def test_assessment_type_who_other_not_required_if_not_specified(self):
        cleaned_data = self.get_valid_assessment_who_other_sv_data(visit_code=DAY03)
        cleaned_data.update(
            {
                "assessment_who": PATIENT,
                "assessment_who_other": "Some other entity",
            }
        )
        self.assertFormValidatorError(
            field="assessment_who_other",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

        cleaned_data.update({"assessment_who_other": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit())
        )

    def test_info_source_raises_error_if_does_not_reconcile_with_patient_assessment(
        self,
    ):
        excluded = [PATIENT, HOSPITAL_NOTES, OUTPATIENT_CARDS, OTHER, NOT_APPLICABLE]
        visit_info_sources = [v[0] for v in VISIT_INFO_SOURCE2 if v[0] not in excluded]
        for info_source in visit_info_sources:
            with self.subTest(info_source=info_source):
                cleaned_data = self.get_valid_in_person_sv_data(visit_code=DAY14)
                cleaned_data.update({"info_source": info_source})
                expected_msg = SubjectVisitFormValidator.get_info_source_mismatch_error_msg(
                    info_source=info_source,
                    assessment_type=cleaned_data.get("assessment_type"),
                    assessment_who=cleaned_data.get("assessment_who"),
                )
                self.assertFormValidatorError(
                    field="info_source",
                    expected_msg=expected_msg,
                    form_validator=self.validate_form_validator(
                        cleaned_data, instance=SubjectVisit()
                    ),
                )

    def test_info_source_raises_error_if_does_not_reconcile_with_nok_telephone_answers(
        self,
    ):
        excluded = [
            PATIENT_REPRESENTATIVE,
            HOSPITAL_NOTES,
            OUTPATIENT_CARDS,
            OTHER,
            NOT_APPLICABLE,
        ]
        visit_info_sources = [v[0] for v in VISIT_INFO_SOURCE2 if v[0] not in excluded]
        for info_source in visit_info_sources:
            with self.subTest(info_source=info_source):
                cleaned_data = self.get_valid_nok_sv_data(visit_code=DAY03)
                cleaned_data.update({"info_source": info_source})
                expected_msg = SubjectVisitFormValidator.get_info_source_mismatch_error_msg(
                    info_source=info_source,
                    assessment_type=cleaned_data.get("assessment_type"),
                    assessment_who=cleaned_data.get("assessment_who"),
                )
                self.assertFormValidatorError(
                    field="info_source",
                    expected_msg=expected_msg,
                    form_validator=self.validate_form_validator(
                        cleaned_data, instance=SubjectVisit()
                    ),
                )

    def test_info_source_raises_error_if_does_not_reconcile_with_other_assessment_type(
        self,
    ):
        excluded = [
            PATIENT_REPRESENTATIVE,
            HOSPITAL_NOTES,
            OUTPATIENT_CARDS,
            OTHER,
            NOT_APPLICABLE,
        ]
        visit_info_sources = [v[0] for v in VISIT_INFO_SOURCE2 if v[0] not in excluded]
        for info_source in visit_info_sources:
            with self.subTest(info_source=info_source):
                cleaned_data = self.get_valid_assessment_type_other_sv_data(visit_code=DAY03)
                cleaned_data.update({"info_source": info_source})
                expected_msg = SubjectVisitFormValidator.get_info_source_mismatch_error_msg(
                    info_source=info_source,
                    assessment_type=cleaned_data.get("assessment_type"),
                    assessment_who=cleaned_data.get("assessment_who"),
                )
                self.assertFormValidatorError(
                    field="info_source",
                    expected_msg=expected_msg,
                    form_validator=self.validate_form_validator(
                        cleaned_data, instance=SubjectVisit()
                    ),
                )

    def test_deceased_status_invalid_at_baseline(self):
        cleaned_data = self.get_valid_in_person_sv_data(visit_code=DAY01)
        cleaned_data.update({"survival_status": DEAD})
        self.assertFormValidatorError(
            field="survival_status",
            expected_msg="Invalid: Cannot be 'Deceased' at baseline",
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

    def test_deceased_status_invalid_for_in_person_visit(self):
        cleaned_data = self.get_valid_in_person_sv_data(visit_code=DAY14)
        cleaned_data.update({"survival_status": DEAD})
        self.assertFormValidatorError(
            field="survival_status",
            expected_msg="Invalid: Expected 'Alive' if this is an 'In person' visit",
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

    def test_deceased_status_invalid_for_patient_telephone_visit(self):
        cleaned_data = self.get_valid_patient_telephone_sv_data(visit_code=DAY03)
        cleaned_data.update({"survival_status": DEAD})
        self.assertFormValidatorError(
            field="survival_status",
            expected_msg="Invalid: Expected 'Alive' if spoke to 'Patient'",
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

    def test_deceased_status_valid_for_other_telephone_visits(self):
        sources = [
            src[0] for src in ASSESSMENT_WHO_CHOICES if src[0] not in [PATIENT, NOT_APPLICABLE]
        ]
        for assessment_who in sources:
            with self.subTest(assessment_who=assessment_who):
                cleaned_data = deepcopy(self.get_valid_nok_sv_data(visit_code=DAY03))
                cleaned_data.update(
                    {
                        "assessment_who": assessment_who,
                        "assessment_who_other": "xxx" if assessment_who == OTHER else "",
                        "survival_status": DEAD,
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(
                        cleaned_data, instance=SubjectVisit()
                    )
                )

    def test_hospitalized_yes_invalid_at_baseline(self):
        cleaned_data = self.get_valid_in_person_sv_data(visit_code=DAY01)
        cleaned_data.update({"hospitalized": YES})
        self.assertFormValidatorError(
            field="hospitalized",
            expected_msg="Invalid. Expected NO at baseline",
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

    def test_hospitalized_unknown_invalid_if_spoke_to_patient(self):
        cleaned_data = self.get_valid_in_person_sv_data(visit_code=DAY01)
        cleaned_data.update(
            {
                "assessment_who": PATIENT,
                "info_source": PATIENT,
                "hospitalized": UNKNOWN,
            }
        )
        self.assertFormValidatorError(
            field="hospitalized",
            expected_msg=(
                "Invalid. Cannot be 'Unknown' if spoke to 'Patient' "
                "or 'Patient' was MAIN source of information"
            ),
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

        cleaned_data.update(
            {
                "assessment_who": PATIENT,
                "info_source": OTHER,
                "info_source_other": "some other information source",
                "hospitalized": UNKNOWN,
            }
        )
        self.assertFormValidatorError(
            field="hospitalized",
            expected_msg=(
                "Invalid. Cannot be 'Unknown' if spoke to 'Patient' "
                "or 'Patient' was MAIN source of information"
            ),
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit()),
        )

    def test_hospitalized_unknown_valid_if_not_patient(self):
        cleaned_data = self.get_valid_nok_sv_data(visit_code=DAY03)
        cleaned_data.update({"hospitalized": UNKNOWN})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit())
        )

        cleaned_data = self.get_valid_assessment_who_other_sv_data(visit_code=DAY03)
        cleaned_data.update({"hospitalized": UNKNOWN})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data, instance=SubjectVisit())
        )


@dataclass
class AssessmentInfoSourceCombo:
    assessment_type: str
    assessment_who: str
    info_source: str


class TestInfoSourceAssessmentTypeWhoValidationLogic(TestCase):
    def test_returns_true_for_valid_choice_combos(self):
        valid_combos = (
            # Valid combos when subject visit info source is 'Patient'
            AssessmentInfoSourceCombo(
                assessment_type=IN_PERSON,
                assessment_who=PATIENT,
                info_source=PATIENT,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=TELEPHONE,
                assessment_who=PATIENT,
                info_source=PATIENT,
            ),
            # Valid combos when subject visit info source is 'Patient Representative'
            AssessmentInfoSourceCombo(
                assessment_type=TELEPHONE,
                assessment_who=NEXT_OF_KIN,
                info_source=PATIENT_REPRESENTATIVE,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=TELEPHONE,
                assessment_who=OTHER,
                info_source=PATIENT_REPRESENTATIVE,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=OTHER,
                assessment_who=OTHER,
                info_source=PATIENT_REPRESENTATIVE,
            ),
            # 'Some' valid combos when subject visit info source is 'Hospital notes',
            # 'Outpatient cards', or 'Other'
            AssessmentInfoSourceCombo(
                assessment_type=OTHER,
                assessment_who=OTHER,
                info_source=HOSPITAL_NOTES,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=OTHER,
                assessment_who=OTHER,
                info_source=OUTPATIENT_CARDS,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=OTHER,
                assessment_who=OTHER,
                info_source=OTHER,
            ),
        )
        for combo in valid_combos:
            with self.subTest(combo=combo):
                self.assertTrue(
                    SubjectVisitFormValidator.info_source_reconciles_with_assessment_type_who(
                        info_source=combo.info_source,
                        assessment_type=combo.assessment_type,
                        assessment_who=combo.assessment_who,
                    )
                )

    def test_returns_false_for_invalid_choice_combos(self):
        invalid_combos = (
            # Invalid combos when subject visit info source is 'Patient'
            AssessmentInfoSourceCombo(
                assessment_type=TELEPHONE,
                assessment_who=NEXT_OF_KIN,
                info_source=PATIENT,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=TELEPHONE,
                assessment_who=OTHER,
                info_source=PATIENT,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=OTHER,
                assessment_who=IN_PERSON,
                info_source=PATIENT,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=OTHER,
                assessment_who=NEXT_OF_KIN,
                info_source=PATIENT,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=OTHER,
                assessment_who=OTHER,
                info_source=PATIENT,
            ),
            # Invalid combos when subject visit info source is 'Patient Representative'
            AssessmentInfoSourceCombo(
                assessment_type=IN_PERSON,
                assessment_who=PATIENT,
                info_source=PATIENT_REPRESENTATIVE,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=IN_PERSON,
                assessment_who=OTHER,
                info_source=PATIENT_REPRESENTATIVE,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=TELEPHONE,
                assessment_who=PATIENT,
                info_source=PATIENT_REPRESENTATIVE,
            ),
            # Invalid combos when subject visit info source is 'Not applicable (if missed)'
            AssessmentInfoSourceCombo(
                assessment_type=IN_PERSON,
                assessment_who=PATIENT,
                info_source=NOT_APPLICABLE,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=TELEPHONE,
                assessment_who=PATIENT,
                info_source=NOT_APPLICABLE,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=TELEPHONE,
                assessment_who=NEXT_OF_KIN,
                info_source=NOT_APPLICABLE,
            ),
            AssessmentInfoSourceCombo(
                assessment_type=OTHER,
                assessment_who=OTHER,
                info_source=NOT_APPLICABLE,
            ),
        )
        for combo in invalid_combos:
            with self.subTest(combo=combo):
                self.assertFalse(
                    SubjectVisitFormValidator.info_source_reconciles_with_assessment_type_who(
                        info_source=combo.info_source,
                        assessment_type=combo.assessment_type,
                        assessment_who=combo.assessment_who,
                    )
                )
