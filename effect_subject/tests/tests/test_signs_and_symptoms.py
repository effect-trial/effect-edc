from copy import deepcopy
from datetime import timedelta
from typing import Optional

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.test import TestCase, tag
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_constants.constants import (
    HEADACHE,
    IN_PERSON,
    NO,
    NOT_APPLICABLE,
    OTHER,
    TELEPHONE,
    UNKNOWN,
    VISUAL_LOSS,
    YES,
)
from edc_constants.disease_constants import (
    CN_PALSY_LEFT_OTHER,
    CN_PALSY_RIGHT_OTHER,
    FOCAL_NEUROLOGIC_DEFICIT_OTHER,
)
from edc_visit_tracking.constants import SCHEDULED
from model_bakery import baker

from effect_lists.models import SiSx
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms import SignsAndSymptomsForm
from effect_subject.forms.signs_and_symptoms_form import SignsAndSymptomsFormValidator
from effect_subject.models import SignsAndSymptoms, SubjectVisit
from effect_subject.tests.tests.mixins import ReportingFieldsetBaselineTestCaseMixin
from effect_visit_schedule.constants import DAY01, DAY14

# TODO: Migrate to effect-form-validator


class SignsSymptomsTestError(Exception):
    pass


@tag("sisx")
class TestSignsAndSymptoms(EffectTestCaseMixin, TestCase):
    def test_ok(self):
        subject_visit = self.get_subject_visit()
        obj = baker.make_recipe("effect_subject.signsandsymptoms", subject_visit=subject_visit)
        form = SignsAndSymptomsForm(instance=obj)
        form.is_valid()

    def test_calculated_headache_duration(self):
        subject_visit = self.get_subject_visit()
        obj = baker.make_recipe("effect_subject.signsandsymptoms", subject_visit=subject_visit)
        self.assertIsNone(obj.calculated_headache_duration)

        obj.headache_duration = "2d"
        obj.save()
        self.assertEqual(obj.calculated_headache_duration, timedelta(days=2))

        obj.headache_duration = "1d12h"
        obj.save()
        self.assertEqual(obj.calculated_headache_duration, timedelta(days=1, hours=12))

        obj.headache_duration = "3h"
        obj.save()
        self.assertEqual(obj.calculated_headache_duration, timedelta(hours=3))

        obj.headache_duration = ""
        obj.save()
        self.assertIsNone(obj.calculated_headache_duration)


@tag("sisx")
class TestSignsAndSymptomsFormValidationBase(EffectTestCaseMixin, TestCase):

    form_validator_cls = SignsAndSymptomsFormValidator
    form_validator_model_cls = SignsAndSymptoms

    def setUp(self):
        super().setUp()
        subject_visit = self.get_subject_visit()  # day01
        subject_visit = self.get_next_subject_visit(subject_visit)  # day03
        subject_visit = self.get_next_subject_visit(subject_visit)  # day09
        self.get_next_subject_visit(subject_visit)  # day14

    @staticmethod
    def get_valid_patient_with_no_signs_or_symptoms(
        visit_code: str = None,
        assessment_type: str = None,
    ):
        visit_code = visit_code or DAY14
        subject_visit = SubjectVisit.objects.get(visit_code=visit_code)
        subject_visit.assessment_type = assessment_type or IN_PERSON
        return {
            "subject_visit": subject_visit,
            "report_datetime": subject_visit.report_datetime,
            "any_sx": NO,
            "current_sx": SiSx.objects.filter(name=NOT_APPLICABLE),
            "current_sx_other": "",
            "cm_sx": NOT_APPLICABLE,
            "current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE),
            "current_sx_gte_g3_other": "",
            "headache_duration": "",
            "cn_palsy_left_other": "",
            "cn_palsy_right_other": "",
            "focal_neurologic_deficit_other": "",
            "visual_field_loss": "",
            "xray_performed": NOT_APPLICABLE if assessment_type == TELEPHONE else NO,
            "lp_performed": NOT_APPLICABLE if assessment_type == TELEPHONE else NO,
            "urinary_lam_performed": NOT_APPLICABLE if assessment_type == TELEPHONE else NO,
            "reportable_as_ae": NOT_APPLICABLE,
            "patient_admitted": NOT_APPLICABLE,
        }

    def get_valid_patient_any_sx_unknown(self, visit_code: str = None):
        cleaned_data = deepcopy(
            self.get_valid_patient_with_no_signs_or_symptoms(
                visit_code=visit_code, assessment_type=TELEPHONE
            )
        )
        cleaned_data.update(
            {
                "any_sx": UNKNOWN,
                "current_sx": SiSx.objects.filter(name=NOT_APPLICABLE),
                "current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE),
                # Cannot be in person visit if "any_sx": UNKNOWN
                # Investigations cannot have been performed if not in person visit
                "xray_performed": NOT_APPLICABLE,
                "lp_performed": NOT_APPLICABLE,
                "urinary_lam_performed": NOT_APPLICABLE,
            }
        )
        return cleaned_data

    def get_valid_patient_with_signs_or_symptoms(
        self,
        visit_code: str = None,
        assessment_type: str = None,
    ):
        visit_code = visit_code or DAY14
        assessment_type = assessment_type or IN_PERSON
        subject_visit = SubjectVisit.objects.get(visit_code=visit_code)
        for v in subject_visit.schedule.visits.timepoints:
            appointment = self.get_appointment(
                subject_identifier=subject_visit.subject_identifier,
                timepoint=v.timepoint,
                visit_code_sequence=0,
            )
            try:
                subject_visit = SubjectVisit.objects.get(appointment=appointment)
            except ObjectDoesNotExist:
                subject_visit = SubjectVisit.objects.create(
                    appointment=appointment,
                    reason=SCHEDULED,
                    report_datetime=appointment.appt_datetime,
                )
            if v.name == visit_code:
                appointment.appt_status = IN_PROGRESS_APPT
                appointment.save()
                appointment.refresh_from_db()
                break
            else:
                appointment.appt_status = INCOMPLETE_APPT
                appointment.save()
                appointment.refresh_from_db()

        if not subject_visit:
            raise SignsSymptomsTestError("subject visit / appointment not found")
        subject_visit.assessment_type = assessment_type
        subject_visit.save()
        subject_visit.refresh_from_db()

        return {
            "subject_visit": subject_visit,
            "report_datetime": subject_visit.report_datetime,
            "any_sx": YES,
            "current_sx": SiSx.objects.filter(Q(name="fever") | Q(name="vomiting")),
            "current_sx_other": "",
            "cm_sx": NO,
            "current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE),
            "current_sx_gte_g3_other": "",
            "headache_duration": "",
            "cn_palsy_left_other": "",
            "cn_palsy_right_other": "",
            "focal_neurologic_deficit_other": "",
            "visual_field_loss": "",
            "xray_performed": YES,
            "lp_performed": YES,
            "urinary_lam_performed": YES,
            "reportable_as_ae": NOT_APPLICABLE if visit_code == DAY01 else NO,
            "patient_admitted": NOT_APPLICABLE if visit_code == DAY01 else NO,
        }

    def get_valid_patient_with_g3_signs_or_symptoms(self, visit_code: str = None):
        cleaned_data = deepcopy(
            self.get_valid_patient_with_signs_or_symptoms(visit_code=visit_code)
        )
        cleaned_data.update(
            {
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
                "current_sx_gte_g3_other": "",
                "reportable_as_ae": NOT_APPLICABLE if visit_code == DAY01 else YES,
            }
        )
        return cleaned_data

    def get_valid_patient_with_cm_symptoms(self, visit_code: str = None):
        cleaned_data = deepcopy(
            self.get_valid_patient_with_g3_signs_or_symptoms(visit_code=visit_code)
        )
        cleaned_data.update({"cm_sx": YES})
        return cleaned_data


class TestSignsAndSymptomsFormValidation(TestSignsAndSymptomsFormValidationBase):
    def test_non_symptomatic_patient_valid_baseline(self):
        cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms(visit_code=DAY01)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_non_symptomatic_patient_valid_d14(self):
        cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms(visit_code=DAY14)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_any_sx_unknown_valid_baseline(self):
        cleaned_data = self.get_valid_patient_any_sx_unknown(visit_code=DAY01)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_any_sx_unknown_valid_d14(self):
        cleaned_data = self.get_valid_patient_any_sx_unknown(visit_code=DAY14)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_patient_with_signs_or_symptoms_baseline(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms(visit_code=DAY01)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_patient_with_signs_or_symptoms_d14(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms(visit_code=DAY14)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_patient_with_g3_signs_or_symptoms_baseline(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms(visit_code=DAY01)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_patient_with_g3_signs_or_symptoms_d14(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms(visit_code=DAY14)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_patient_with_cm_symptoms_baseline(self):
        cleaned_data = self.get_valid_patient_with_cm_symptoms(visit_code=DAY01)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_patient_with_cm_symptoms_d14(self):
        cleaned_data = self.get_valid_patient_with_cm_symptoms(visit_code=DAY14)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_m2m_sx_selections_expect_na_if_any_sx_is_no(self):
        cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": NO,
                "current_sx": SiSx.objects.filter(name="fever"),
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
            }
        )
        self.assertFormValidatorError(
            field="current_sx",
            expected_msg="Expected '--Not applicable' only.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(name=NOT_APPLICABLE),
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3",
            expected_msg="Expected '--Not applicable' only.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE)})
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_m2m_sx_selections_expect_na_if_any_sx_is_unknown(self):
        cleaned_data = self.get_valid_patient_any_sx_unknown()
        cleaned_data.update(
            {
                "any_sx": UNKNOWN,
                "current_sx": SiSx.objects.filter(name="fever"),
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
            }
        )
        self.assertFormValidatorError(
            field="current_sx",
            expected_msg="Expected '--Not applicable' only.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(name=NOT_APPLICABLE),
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3",
            expected_msg="Expected '--Not applicable' only.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE)})
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_m2m_current_sx_with_na_invalid_if_any_sx_is_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": YES,
                "current_sx": SiSx.objects.filter(Q(name="fever") | Q(name=NOT_APPLICABLE)),
            }
        )
        self.assertFormValidatorError(
            field="current_sx",
            expected_msg="Invalid selection. Cannot be any of: --Not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(Q(name=NOT_APPLICABLE)),
            }
        )
        self.assertFormValidatorError(
            field="current_sx",
            expected_msg="Invalid selection. Cannot be any of: --Not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx": SiSx.objects.filter(Q(name="fever"))})
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_m2m_current_sx_gte_g3_can_be_na_if_any_sx_is_yes(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": YES,
                "current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE),
                "reportable_as_ae": NO,
            }
        )
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_m2m_current_sx_gte_g3_cannot_be_na_with_another_selection(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": YES,
                "current_sx_gte_g3": SiSx.objects.filter(
                    Q(name="fever") | Q(name=NOT_APPLICABLE)
                ),
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3",
            expected_msg=(
                "Invalid combination. "
                "'--Not applicable' may not be combined with other selections"
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3": SiSx.objects.filter(Q(name="fever"))})
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

        cleaned_data.update(
            {
                "current_sx_gte_g3": SiSx.objects.filter(Q(name=NOT_APPLICABLE)),
                "reportable_as_ae": NO,
            }
        )
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_m2m_sx_valid_with_multiple_selections_if_any_sx_is_yes(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": YES,
                "current_sx": SiSx.objects.filter(
                    Q(name="fever")
                    | Q(name="vomiting")
                    | Q(name=OTHER)
                    | Q(name=VISUAL_LOSS)
                    | Q(name="headache")
                ),
                "current_sx_gte_g3": SiSx.objects.filter(
                    Q(name="fever")
                    | Q(name="vomiting")
                    | Q(name=OTHER)
                    | Q(name=VISUAL_LOSS)
                    | Q(name="headache")
                ),
                "current_sx_other": "Some other sx",
                "current_sx_gte_g3_other": "Some other sx",
                "headache_duration": "2d",
                "visual_field_loss": "Visual field loss details",
            }
        )
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_current_sx_other_required_if_other_selected(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(name=OTHER),
                "current_sx_other": "",
            }
        )
        self.assertFormValidatorError(
            field="current_sx_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_other": "Some other sx"})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_current_sx_other_not_required_if_other_not_selected(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(name="fever"),
                "current_sx_other": "Some other sx",
            }
        )
        self.assertFormValidatorError(
            field="current_sx_other",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_other": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_reportable_as_ae_applicable_if_any_sx_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": YES,
                "reportable_as_ae": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="reportable_as_ae",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        for answer in [YES, NO]:
            with self.subTest(answer=answer):
                cleaned_data.update(
                    {
                        "current_sx_gte_g3": SiSx.objects.filter(name="fever")
                        if answer == YES
                        else SiSx.objects.filter(name=NOT_APPLICABLE),
                        "reportable_as_ae": answer,
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_reportable_as_ae_not_applicable_if_any_sx_not_yes(self):
        for any_sx_answer in [NO, UNKNOWN]:
            for reportable_as_ae_answer in [YES, NO]:
                with self.subTest(
                    any_sx_answer=any_sx_answer,
                    reportable_as_ae_answer=reportable_as_ae_answer,
                ):
                    cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms(
                        visit_code=DAY14,
                        assessment_type=TELEPHONE if any_sx_answer == UNKNOWN else IN_PERSON,
                    )
                    cleaned_data.update(
                        {
                            "any_sx": any_sx_answer,
                            "current_sx": SiSx.objects.filter(name=NOT_APPLICABLE),
                            "current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE),
                            "reportable_as_ae": reportable_as_ae_answer,
                        }
                    )
                    self.assertFormValidatorError(
                        field="reportable_as_ae",
                        expected_msg="This field is not applicable.",
                        form_validator=self.validate_form_validator(cleaned_data),
                    )

                    cleaned_data.update({"reportable_as_ae": NOT_APPLICABLE})
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data)
                    )

    def test_reportable_as_ae_if_current_sx_gte_g3s(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
                "reportable_as_ae": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="reportable_as_ae",
            expected_msg="This field is applicable",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"reportable_as_ae": NO})
        self.assertFormValidatorError(
            field="reportable_as_ae",
            expected_msg=(
                "Invalid selection. "
                "Expected 'Yes', if symptoms Grade 3 or above were reported"
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"reportable_as_ae": YES})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_reportable_as_ae_if_no_current_sx_gte_g3(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE),
                "reportable_as_ae": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="reportable_as_ae",
            expected_msg="This field is applicable",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"reportable_as_ae": YES})
        self.assertFormValidatorError(
            field="reportable_as_ae",
            expected_msg=(
                "Invalid selection. "
                "Expected 'No', if no symptoms at Grade 3 or above were reported."
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"reportable_as_ae": NO})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_reportable_as_ae_yes_invalid_if_sx_gte_g3_na(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update({"reportable_as_ae": YES})
        self.assertFormValidatorError(
            field="reportable_as_ae",
            expected_msg=(
                "Invalid selection. "
                "Expected 'No', if no symptoms at Grade 3 or above were reported."
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"reportable_as_ae": NO})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_reportable_as_ae_no_invalid_if_sx_gte_g3(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update({"reportable_as_ae": NO})
        self.assertFormValidatorError(
            field="reportable_as_ae",
            expected_msg=(
                "Invalid selection. "
                "Expected 'Yes', if symptoms Grade 3 or above were reported."
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"reportable_as_ae": YES})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_can_opt_out_of_current_sx_gte_g3_if_any_sx_is_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update({"current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE)})

        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_sx_gte_g3_with_no_current_sx_raises_error(self):
        cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": NO,
                "current_sx": SiSx.objects.filter(name=NOT_APPLICABLE),
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3",
            expected_msg="Expected '--Not applicable' only.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE)})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_sx_gte_g3_not_in_current_sx_raises_error(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(Q(name="fever") | Q(name="vomiting")),
                "current_sx_gte_g3": SiSx.objects.filter(name="cough"),
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3",
            expected_msg="Invalid selection. Must be from above list of signs and symptoms",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(
                    Q(name="fever") | Q(name="vomiting") | Q(name="cough")
                ),
            }
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_other_not_in_current_sx_gte_g3_when_other_in_current_sx_raises_error(
        self,
    ):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(name=OTHER),
                "current_sx_other": "Some other sx",
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3",
            expected_msg="Invalid selection. Must be from above list of signs and symptoms",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3": SiSx.objects.filter(name=OTHER)})
        self.assertFormValidatorError(
            field="current_sx_gte_g3_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3_other": "Some other G3 sx"})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_sx_gte_g3_superset_of_current_sx_raises_error(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(Q(name="fever") | Q(name="vomiting")),
                "current_sx_gte_g3": SiSx.objects.filter(
                    Q(name="fever") | Q(name="vomiting") | Q(name="cough")
                ),
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3",
            expected_msg="Invalid selection. Must be from above list of signs and symptoms",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(
                    Q(name="fever") | Q(name="vomiting") | Q(name="cough")
                ),
            }
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_sx_gte_g3_subset_of_current_sx_valid(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(
                    Q(name="fever") | Q(name="vomiting") | Q(name="cough")
                ),
                "current_sx_gte_g3": SiSx.objects.filter(Q(name="fever") | Q(name="vomiting")),
            }
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_current_sx_gte_g3_other_field_required_if_g3_other_selected(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(name=OTHER),
                "current_sx_other": "Some other sx",
                "current_sx_gte_g3": SiSx.objects.filter(name=OTHER),
                "current_sx_gte_g3_other": "",
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3_other": "Some other G3 sx"})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_current_sx_gte_g3_other_not_required_if_other_not_selected(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
                "current_sx_gte_g3_other": "Some other sx",
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3_other",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3_other": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_validate_current_sx_other_specify_fields_required_if_specified(self):
        sx_selection_other_fields = [
            (HEADACHE, "headache_duration"),
            (CN_PALSY_LEFT_OTHER, "cn_palsy_left_other"),
            (CN_PALSY_RIGHT_OTHER, "cn_palsy_right_other"),
            (FOCAL_NEUROLOGIC_DEFICIT_OTHER, "focal_neurologic_deficit_other"),
            (VISUAL_LOSS, "visual_field_loss"),
        ]

        for sx_selection, other_field in sx_selection_other_fields:
            with self.subTest(sx_selection=sx_selection, other_field=other_field):
                cleaned_data = deepcopy(self.get_valid_patient_with_signs_or_symptoms())
                cleaned_data.update({"current_sx": SiSx.objects.filter(name=sx_selection)})
                self.assertFormValidatorError(
                    field=other_field,
                    expected_msg="This field is required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

                cleaned_data.update(
                    {
                        other_field: "3d"
                        if other_field == "headache_duration"
                        else "Some other text"
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_validate_current_sx_other_specify_fields_not_required_if_not_specified(
        self,
    ):
        other_fields = [
            "headache_duration",
            "cn_palsy_left_other",
            "cn_palsy_right_other",
            "focal_neurologic_deficit_other",
            "visual_field_loss",
        ]

        for other_field in other_fields:
            with self.subTest(other_field=other_field):
                cleaned_data = deepcopy(self.get_valid_patient_with_signs_or_symptoms())
                cleaned_data.update({other_field: "Some other text"})
                self.assertFormValidatorError(
                    field=other_field,
                    expected_msg="This field is not required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

                cleaned_data.update({other_field: ""})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_patient_admitted_applicable_if_any_sx_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": YES,
                "current_sx": SiSx.objects.filter(name="fever"),
                "patient_admitted": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="patient_admitted",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        for answer in [YES, NO]:
            with self.subTest(answer=answer):
                cleaned_data.update({"patient_admitted": answer})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_patient_admitted_not_applicable_if_any_sx_not_yes(self):
        for any_sx_answer in [NO, UNKNOWN]:
            for patient_admitted_answer in [YES, NO]:
                with self.subTest(
                    any_sx_answer=any_sx_answer,
                    patient_admitted_answer=patient_admitted_answer,
                ):
                    cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms(
                        assessment_type=TELEPHONE if any_sx_answer == UNKNOWN else IN_PERSON
                    )
                    cleaned_data.update(
                        {
                            "any_sx": any_sx_answer,
                            "current_sx": SiSx.objects.filter(name=NOT_APPLICABLE),
                            "current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE),
                            "patient_admitted": patient_admitted_answer,
                        }
                    )
                    self.assertFormValidatorError(
                        field="patient_admitted",
                        expected_msg="This field is not applicable.",
                        form_validator=self.validate_form_validator(cleaned_data),
                    )

                    cleaned_data.update({"patient_admitted": NOT_APPLICABLE})
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data)
                    )

    def test_cm_sx_applicable_if_any_sx_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": YES,
                "cm_sx": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="cm_sx",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        for answer in [YES, NO]:
            with self.subTest(answer=answer):
                cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
                cleaned_data.update({"cm_sx": answer})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_cm_sx_not_applicable_if_any_sx_not_yes(self):
        for any_sx_answer in [NO, UNKNOWN]:
            for cm_sx_answer in [YES, NO]:
                with self.subTest(
                    any_sx_answer=any_sx_answer,
                    cm_sx_answer=cm_sx_answer,
                ):
                    cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms(
                        assessment_type=TELEPHONE if any_sx_answer == UNKNOWN else IN_PERSON
                    )
                    cleaned_data.update(
                        {
                            "any_sx": any_sx_answer,
                            "current_sx": SiSx.objects.filter(name=NOT_APPLICABLE),
                            "current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE),
                            "cm_sx": cm_sx_answer,
                        }
                    )
                    self.assertFormValidatorError(
                        field="cm_sx",
                        expected_msg="This field is not applicable.",
                        form_validator=self.validate_form_validator(cleaned_data),
                    )

                    cleaned_data.update({"cm_sx": NOT_APPLICABLE})
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data)
                    )


class TestSignsAndSymptomsStatusReportingFieldsetFormValidation(
    ReportingFieldsetBaselineTestCaseMixin,
    TestSignsAndSymptomsFormValidationBase,
):
    def default_cleaned_data(self, visit_code: Optional[str] = None) -> dict:
        return self.get_valid_patient_with_signs_or_symptoms(visit_code=visit_code)

    def test_reportable_as_ae_allowed_at_d14(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms(visit_code=DAY14)
        cleaned_data.update(
            {
                "reportable_as_ae": YES,
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
            }
        )

        form_validator = self.form_validator_cls(
            cleaned_data=cleaned_data, model=SignsAndSymptoms
        )
        form_validator.validate()
        self.assertDictEqual({}, form_validator._errors)

        cleaned_data.update(
            {
                "reportable_as_ae": NO,
                "current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE),
            }
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_reportable_as_ae_not_required_if_sx_unknown_at_d14(self):
        cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms(
            visit_code=DAY14, assessment_type=TELEPHONE
        )
        cleaned_data.update(
            {
                "any_sx": UNKNOWN,
                "current_sx": SiSx.objects.filter(name=NOT_APPLICABLE),
                "current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE),
                "reportable_as_ae": NOT_APPLICABLE,
            }
        )
        form_validator = self.form_validator_cls(
            cleaned_data=cleaned_data, model=SignsAndSymptoms
        )
        try:
            form_validator.validate()
        except forms.ValidationError as e:
            self.fail(f"ValidationError unexpectedly raised. Got {e}")

    def test_patient_admitted_allowed_at_d14(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms(visit_code=DAY14)
        for response in [YES, NO]:
            with self.subTest(patient_admitted=response):
                cleaned_data.update({"patient_admitted": response})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_patient_admitted_not_required_at_d14(self):
        cleaned_data = self.get_valid_patient_any_sx_unknown()
        cleaned_data.update({"patient_admitted": NOT_APPLICABLE})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )
