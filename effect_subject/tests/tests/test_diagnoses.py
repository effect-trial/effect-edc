from copy import deepcopy

from django.db.models import Q
from django.test import TestCase, tag
from edc_constants.constants import NO, NOT_APPLICABLE, OTHER, YES
from model_bakery import baker

from effect_lists.models import Dx
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.diagnoses_form import DiagnosesForm, DiagnosesFormValidator
from effect_visit_schedule.constants import DAY01, DAY14

from .mixins import ReportingFieldsetDay14TestCaseMixin


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

    def get_d14_visit(self):
        baseline_visit = self.get_subject_visit()
        d3_visit = self.get_next_subject_visit(baseline_visit)
        d9_visit = self.get_next_subject_visit(d3_visit)
        return self.get_next_subject_visit(d9_visit)

    def get_cleaned_data_no_dx(self, visit_code: str = None):
        # Significant Diagnoses CRF only applicable/required at D14
        subject_visit = self.get_d14_visit()
        return {
            "subject_visit": subject_visit,
            "appointment": subject_visit.appointment,
            "gi_side_effects": NO,
            "gi_side_effects_details": "",
            "has_diagnoses": NO,
            "diagnoses": Dx.objects.filter(name=NOT_APPLICABLE),
            "diagnoses_other": "",
            "reportable_as_ae": NOT_APPLICABLE,
            "patient_admitted": NOT_APPLICABLE,
        }

    def get_cleaned_data_with_dx(self, visit_code: str = None):
        cleaned_data = deepcopy(self.get_cleaned_data_no_dx())
        cleaned_data.update(
            {
                "has_diagnoses": YES,
                "diagnoses": Dx.objects.filter(name="malaria"),
                "reportable_as_ae": NO,
                "patient_admitted": NO,
            }
        )
        return cleaned_data


@tag("dx")
class TestDiagnosesFormValidation(TestDiagnosesFormValidationBase):
    def test_d14_cleaned_data_no_dx_ok(self):
        cleaned_data = self.get_cleaned_data_no_dx()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_d14_cleaned_data_with_dx_ok(self):
        cleaned_data = self.get_cleaned_data_with_dx()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_diagnoses_na_if_has_diagnoses_no(self):
        cleaned_data = self.get_cleaned_data_no_dx()
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
        cleaned_data = self.get_cleaned_data_no_dx()
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
        cleaned_data = self.get_cleaned_data_no_dx()
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
        cleaned_data = self.get_cleaned_data_no_dx()
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
        cleaned_data = self.get_cleaned_data_with_dx()
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
        cleaned_data = self.get_cleaned_data_with_dx()
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
    ReportingFieldsetDay14TestCaseMixin,
    TestDiagnosesFormValidationBase,
):
    default_cleaned_data = TestDiagnosesFormValidationBase.get_cleaned_data_with_dx

    def test_reporting_fieldset_ok_if_dx(self):
        cleaned_data = self.get_cleaned_data_with_dx()
        for ae_answer in [YES, NO]:
            for admitted_answer in [YES, NO]:
                with self.subTest(ae_answer=ae_answer, admitted_answer=admitted_answer):
                    cleaned_data.update(
                        {
                            "has_diagnoses": YES,
                            "diagnoses": Dx.objects.filter(name="bacteraemia"),
                            "reportable_as_ae": ae_answer,
                            "patient_admitted": admitted_answer,
                        }
                    )
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data)
                    )

    def test_reporting_fieldset_applicable_if_dx(self):
        cleaned_data = self.get_cleaned_data_with_dx()
        cleaned_data.update(
            {
                "has_diagnoses": YES,
                "diagnoses": Dx.objects.filter(name="bacteraemia"),
                "reportable_as_ae": NOT_APPLICABLE,
                "patient_admitted": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="reportable_as_ae",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "reportable_as_ae": NO,
                "patient_admitted": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="patient_admitted",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "reportable_as_ae": NO,
                "patient_admitted": YES,
            }
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_reporting_fieldset_na_if_no_dx(self):
        cleaned_data = self.get_cleaned_data_no_dx()
        cleaned_data.update(
            {
                "has_diagnoses": NO,
                "diagnoses": Dx.objects.filter(name=""),
                "reportable_as_ae": NO,
                "patient_admitted": NO,
            }
        )
        self.assertFormValidatorError(
            field="reportable_as_ae",
            expected_msg="This field is not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "reportable_as_ae": NOT_APPLICABLE,
                "patient_admitted": YES,
            }
        )
        self.assertFormValidatorError(
            field="patient_admitted",
            expected_msg="This field is not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "reportable_as_ae": NOT_APPLICABLE,
                "patient_admitted": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )
