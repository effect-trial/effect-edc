from django.db.models import Q
from django.test import TestCase, tag
from edc_constants.constants import NO, NOT_APPLICABLE, OTHER, YES
from model_bakery import baker

from effect_lists.models import Dx
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.diagnoses_form import DiagnosesForm, DiagnosesFormValidator
from effect_visit_schedule.constants import DAY01, DAY14

from .mixins import ReportingFieldsetBaselineTestCaseMixin


@tag("dx")
class TestDiagnoses(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def test_ok(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)  # d3
        subject_visit = self.get_next_subject_visit(subject_visit)  # d9
        subject_visit = self.get_next_subject_visit(subject_visit)  # d14
        obj = baker.make_recipe(
            "effect_subject.diagnoses",
            subject_visit=subject_visit,
        )
        form = DiagnosesForm(instance=obj)
        form.is_valid()


@tag("dx")
class TestDiagnosesFormValidationBase(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = DiagnosesFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_valid_diagnoses_data(self, visit_code: str = DAY01):
        self.subject_visit.appointment.visit_code = visit_code
        return {
            "subject_visit": self.subject_visit,
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "gi_side_effects": NO,
            "gi_side_effects_details": "",
            "has_diagnoses": NO,
            "diagnoses": Dx.objects.filter(name=""),  # TODO check:
            "diagnoses_other": "",
            "reportable_as_ae": NOT_APPLICABLE if visit_code == DAY01 else NO,
            "patient_admitted": NOT_APPLICABLE if visit_code == DAY01 else NO,
        }


@tag("dx")
class TestDiagnosesFormValidation(TestDiagnosesFormValidationBase):
    def test_baseline_valid_diagnoses_data_valid(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY01)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_d14_valid_diagnoses_data_valid(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY14)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_diagnoses_applicable_if_has_diagnoses_yes(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY14)
        cleaned_data.update(
            {
                "has_diagnoses": YES,
                "diagnoses": Dx.objects.filter(name="malaria"),
            }
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_diagnoses_na_if_has_diagnoses_no(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY14)
        cleaned_data.update(
            {
                "has_diagnoses": NO,
                "diagnoses": Dx.objects.filter(name=NOT_APPLICABLE),
            }
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_diagnoses_na_raises_if_has_diagnoses_yes(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY14)
        cleaned_data.update(
            {
                "has_diagnoses": YES,
                "diagnoses": Dx.objects.filter(name=NOT_APPLICABLE),
            }
        )
        self.assertFormValidatorError(
            field="diagnoses",
            expected_msg=(
                "Invalid selection. "
                "Cannot be N/A if there are significant diagnoses to report."
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_diagnoses_specified_raises_if_has_diagnoses_no(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY14)
        cleaned_data.update(
            {
                "has_diagnoses": NO,
                "diagnoses": Dx.objects.filter(name="malaria"),
            }
        )
        self.assertFormValidatorError(
            field="diagnoses",
            expected_msg="Expected N/A only if NO significant diagnoses to report.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cannot_list_other_diagnoses_with_na(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY14)
        cleaned_data.update(
            {
                "has_diagnoses": NO,
                "diagnoses": Dx.objects.filter(
                    Q(name=NOT_APPLICABLE) | Q(name="malaria") | Q(name="bacteraemia")
                ),
            }
        )
        self.assertFormValidatorError(
            field="diagnoses",
            expected_msg="Expected N/A only if NO significant diagnoses to report.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "has_diagnoses": NO,
                "diagnoses": Dx.objects.filter(
                    Q(name=NOT_APPLICABLE) | Q(name="malaria")
                ),
            }
        )
        self.assertFormValidatorError(
            field="diagnoses",
            expected_msg="Expected N/A only if NO significant diagnoses to report.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "has_diagnoses": NO,
                "diagnoses": Dx.objects.filter(Q(name=NOT_APPLICABLE)),
            }
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_diagnoses_other_required_if_specified(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY14)
        cleaned_data.update(
            {
                "has_diagnoses": YES,
                "diagnoses": Dx.objects.filter(
                    Q(name=OTHER) | Q(name="malaria") | Q(name="bacteraemia")
                ),
            }
        )
        self.assertFormValidatorError(
            field="diagnoses_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"diagnoses_other": "Some other dx"})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_diagnoses_other_not_required_if_not_specified(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY14)
        cleaned_data.update(
            {
                "has_diagnoses": YES,
                "diagnoses": Dx.objects.filter(
                    Q(name="malaria") | Q(name="bacteraemia")
                ),
                "diagnoses_other": "Some other dx",
            }
        )
        self.assertFormValidatorError(
            field="diagnoses_other",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"diagnoses_other": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data),
        )


@tag("dx")
class TestDiagnosesReportingFieldsetFormValidation(
    ReportingFieldsetBaselineTestCaseMixin,
    TestDiagnosesFormValidationBase,
):
    default_cleaned_data = TestDiagnosesFormValidationBase.get_valid_diagnoses_data

    def test_reportable_as_ae_allowed_at_d14(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY14)
        cleaned_data.update({"reportable_as_ae": YES})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )
        cleaned_data.update({"reportable_as_ae": NO})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_reportable_as_ae_not_required_at_d14(self):
        cleaned_data = self.get_valid_diagnoses_data()
        cleaned_data.update({"reportable_as_ae": NOT_APPLICABLE})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_patient_admitted_allowed_at_d14(self):
        cleaned_data = self.get_valid_diagnoses_data(visit_code=DAY14)
        for response in [YES, NO]:
            with self.subTest(patient_admitted=response):
                cleaned_data.update({"patient_admitted": response})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_patient_admitted_not_required_at_d14(self):
        cleaned_data = self.get_valid_diagnoses_data()
        cleaned_data.update({"patient_admitted": NOT_APPLICABLE})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )
