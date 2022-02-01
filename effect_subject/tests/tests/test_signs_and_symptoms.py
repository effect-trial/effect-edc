from copy import deepcopy

from django.db.models import Q
from django.test import TestCase, tag
from edc_constants.choices import YES_NO_UNKNOWN
from edc_constants.constants import NO, NOT_APPLICABLE, UNKNOWN, YES
from model_bakery import baker

from effect_lists.models import SiSx
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.constants import HEADACHE, VISUAL_LOSS
from effect_subject.forms import SignsAndSymptomsForm
from effect_subject.forms.signs_and_symptoms_form import SignsAndSymptomsFormValidator


@tag("sas")
class TestFollowup(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def test_ok(self):
        subject_visit = self.subject_visit
        obj = baker.make_recipe(
            "effect_subject.signsandsymptoms", subject_visit=subject_visit
        )
        form = SignsAndSymptomsForm(instance=obj)
        form.is_valid()


@tag("sas")
class TestFollowupFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = SignsAndSymptomsFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    # TODO: Test any_signs_symptoms == Unknown
    # TODO: Test patient with signs and symptoms is valid

    def get_valid_patient_with_no_signs_or_symptoms(self):
        return {
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "any_signs_symptoms": NO,
            "signs_and_symptoms": SiSx.objects.none(),
            "signs_and_symptoms_gte_g3": SiSx.objects.none(),
            "headache_duration": "",
            "visual_field_loss": "",
            "reportable_as_ae": NOT_APPLICABLE,
            "patient_admitted": NOT_APPLICABLE,
            "cm_signs_symptoms": NOT_APPLICABLE,
        }

    def get_valid_patient_any_signs_or_symptoms_unknown(self):
        cleaned_data = deepcopy(self.get_valid_patient_with_no_signs_or_symptoms())
        cleaned_data.update(
            {
                "any_signs_symptoms": UNKNOWN,
                "signs_and_symptoms": SiSx.objects.none(),
                "signs_and_symptoms_gte_g3": SiSx.objects.none(),
            }
        )
        return cleaned_data

    def get_valid_patient_with_signs_or_symptoms(self):
        return {
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "any_signs_symptoms": YES,
            "signs_and_symptoms": SiSx.objects.filter(
                Q(name="fever") | Q(name="vomiting")
            ),
            "signs_and_symptoms_gte_g3": SiSx.objects.none(),
            "headache_duration": "",
            "visual_field_loss": "",
            "reportable_as_ae": NO,
            "patient_admitted": NO,
            "cm_signs_symptoms": NO,
        }

    def get_valid_patient_with_g3_signs_or_symptoms(self):
        cleaned_data = deepcopy(self.get_valid_patient_with_signs_or_symptoms())
        cleaned_data.update(
            {
                "signs_and_symptoms_gte_g3": SiSx.objects.filter(name="fever"),
                "reportable_as_ae": YES,
            }
        )
        return cleaned_data

    def test_non_symptomatic_patient_valid(self):
        cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_unknown_any_sas(self):
        cleaned_data = self.get_valid_patient_any_signs_or_symptoms_unknown()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_patient_with_signs_or_symptoms(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_valid_patient_with_g3_signs_or_symptoms(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_m2m_signs_and_symptoms_not_required_if_any_sas_is_not_yes(self):
        any_sas_answers = [ans for ans, _ in YES_NO_UNKNOWN if ans != YES]
        for answer in any_sas_answers:
            with self.subTest(answer=answer):
                cleaned_data = self.get_valid_patient_any_signs_or_symptoms_unknown()
                cleaned_data.update(
                    {
                        "any_signs_symptoms": answer,
                        "signs_and_symptoms": SiSx.objects.filter(name="fever"),
                    }
                )
                self.assertFormValidatorError(
                    field="signs_and_symptoms",
                    expected_msg="This field is not required",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

        cleaned_data.update({"signs_and_symptoms": SiSx.objects.none()})
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_m2m_signs_and_symptoms_required_if_any_sas_is_yes(self):
        cleaned_data = self.get_valid_patient_any_signs_or_symptoms_unknown()
        cleaned_data.update(
            {
                "any_signs_symptoms": YES,
                "signs_and_symptoms": SiSx.objects.none(),
            }
        )
        self.assertFormValidatorError(
            field="signs_and_symptoms",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_reportable_as_ae_applicable_if_any_signs_symptoms_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_signs_symptoms": YES,
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
                        "signs_and_symptoms_gte_g3": SiSx.objects.filter(name="fever")
                        if answer == YES
                        else SiSx.objects.none(),
                        "reportable_as_ae": answer,
                    }
                )
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_reportable_as_ae_not_applicable_if_any_signs_symptoms_not_yes(self):
        for any_sas_answer in [NO, UNKNOWN]:
            for reportable_as_ae_answer in [YES, NO]:
                with self.subTest(
                    any_sas_answer=any_sas_answer,
                    reportable_as_ae_answer=reportable_as_ae_answer,
                ):
                    cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
                    cleaned_data.update(
                        {
                            "any_signs_symptoms": any_sas_answer,
                            "signs_and_symptoms": SiSx.objects.none(),
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

    def test_signs_and_symptoms_gte_g3_not_required_if_reportable_as_ae_is_not_yes(
        self,
    ):
        for reportable_as_ae_answer in [NO, NOT_APPLICABLE]:
            with self.subTest(reportable_as_ae_answer=reportable_as_ae_answer):
                cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
                cleaned_data.update(
                    {"signs_and_symptoms_gte_g3": SiSx.objects.filter(name="fever")}
                )

                self.assertFormValidatorError(
                    field="signs_and_symptoms_gte_g3",
                    expected_msg="This field is not required",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

                cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
                cleaned_data.update({"signs_and_symptoms_gte_g3": SiSx.objects.none()})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_signs_and_symptoms_gte_g3_required_if_reportable_as_ae_is_yes(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "signs_and_symptoms_gte_g3": SiSx.objects.none(),
                "reportable_as_as": YES,
            }
        )
        self.assertFormValidatorError(
            field="signs_and_symptoms_gte_g3",
            expected_msg="This field is required",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {"signs_and_symptoms_gte_g3": SiSx.objects.filter(name="fever")}
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_signs_and_symptoms_gte_g3_not_required_if_any_sas_is_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update({"signs_and_symptoms_gte_g3": SiSx.objects.none()})

        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_headache_duration_applicable_if_in_signs_and_symptoms(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "signs_and_symptoms": SiSx.objects.filter(name=HEADACHE),
                "headache_duration": "",
            }
        )
        self.assertFormValidatorError(
            field="headache_duration",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"headache_duration": "2d3h"})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_headache_duration_not_applicable_if_not_in_signs_and_symptoms(self):
        cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
        cleaned_data.update({"headache_duration": "2d3h"})
        self.assertFormValidatorError(
            field="headache_duration",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        cleaned_data.update({"headache_duration": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update({"headache_duration": "2d3h"})
        self.assertFormValidatorError(
            field="headache_duration",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        cleaned_data.update({"headache_duration": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_visual_field_loss_applicable_if_in_signs_and_symptoms(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "signs_and_symptoms": SiSx.objects.filter(name=VISUAL_LOSS),
                "visual_field_loss": "",
            }
        )
        self.assertFormValidatorError(
            field="visual_field_loss",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"visual_field_loss": "Details on visual field loss"})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_visual_field_loss_not_applicable_if_not_in_signs_and_symptoms(self):
        cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
        cleaned_data.update({"visual_field_loss": "Details on visual field loss"})
        self.assertFormValidatorError(
            field="visual_field_loss",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        cleaned_data.update({"visual_field_loss": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update({"visual_field_loss": "Details on visual field loss"})
        self.assertFormValidatorError(
            field="visual_field_loss",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )
        cleaned_data.update({"visual_field_loss": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_patient_admitted_applicable_if_any_signs_symptoms_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_signs_symptoms": YES,
                "signs_and_symptoms": SiSx.objects.filter(name="fever"),
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

    def test_patient_admitted_not_applicable_if_any_signs_symptoms_not_yes(self):
        for any_sas_answer in [NO, UNKNOWN]:
            for patient_admitted_answer in [YES, NO]:
                with self.subTest(
                    any_sas_answer=any_sas_answer,
                    patient_admitted_answer=patient_admitted_answer,
                ):
                    cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
                    cleaned_data.update(
                        {
                            "any_signs_symptoms": any_sas_answer,
                            "signs_and_symptoms": SiSx.objects.none(),
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

    def test_cm_signs_symptoms_applicable_if_any_signs_symptoms_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_signs_symptoms": YES,
                "signs_and_symptoms": SiSx.objects.filter(
                    Q(name="fever") | Q(name="vomiting")
                ),
                "patient_admitted": NO,
                "cm_signs_symptoms": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="cm_signs_symptoms",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        for answer in [YES, NO]:
            with self.subTest(answer=answer):
                cleaned_data.update({"cm_signs_symptoms": answer})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_cm_signs_symptoms_not_applicable_if_any_signs_symptoms_not_yes(self):
        for any_sas_answer in [NO, UNKNOWN]:
            for cm_signs_symptoms_answer in [YES, NO]:
                with self.subTest(
                    any_sas_answer=any_sas_answer,
                    cm_signs_symptoms_answer=cm_signs_symptoms_answer,
                ):
                    cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
                    cleaned_data.update(
                        {
                            "any_signs_symptoms": any_sas_answer,
                            "signs_and_symptoms": SiSx.objects.none(),
                            "cm_signs_symptoms": cm_signs_symptoms_answer,
                        }
                    )
                    self.assertFormValidatorError(
                        field="cm_signs_symptoms",
                        expected_msg="This field is not applicable.",
                        form_validator=self.validate_form_validator(cleaned_data),
                    )

                    cleaned_data.update({"cm_signs_symptoms": NOT_APPLICABLE})
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data)
                    )
