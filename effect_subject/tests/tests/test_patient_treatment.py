from copy import deepcopy

from django.test import TestCase, tag
from edc_constants.constants import NO, NOT_APPLICABLE, OTHER, YES
from model_bakery import baker

from effect_lists.list_data import list_data
from effect_lists.models import Antibiotics, Drugs, TbTreatments
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms import PatientTreatmentForm
from effect_subject.forms.patient_treatment_form import PatientTreatmentFormValidator


@tag("pt")
class TestPatientTreatment(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def test_ok(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)  # d3
        subject_visit = self.get_next_subject_visit(subject_visit)  # d9
        subject_visit = self.get_next_subject_visit(subject_visit)  # d14
        obj = baker.make_recipe(
            "effect_subject.patienttreatment", subject_visit=subject_visit
        )
        form = PatientTreatmentForm(instance=obj)
        form.is_valid()


@tag("pt")
class TestPatientTreatmentFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = PatientTreatmentFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_cleaned_data_patient_no_cm_no_tx(self):
        return {
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "lp_completed": NO,
            "cm_confirmed": NOT_APPLICABLE,
            "cm_tx": NOT_APPLICABLE,
            "cm_tx_given": NOT_APPLICABLE,
            "cm_tx_given_other": "",
            "tb_tx": NO,
            "tb_tx_date": None,
            "tb_tx_given": TbTreatments.objects.none(),
            "tb_tx_given_other": "",
            "tb_tx_reason_no": "contraindicated",
            "tb_tx_reason_no_other": "",
            "steroids": NO,
            "steroids_date": None,
            "steroids_given": NOT_APPLICABLE,
            "steroids_given_other": "",
            "steroids_course": None,
            "co_trimoxazole": NO,
            "co_trimoxazole_date": None,
            "co_trimoxazole_reason_no": "deferred_local_clinic",
            "co_trimoxazole_reason_no_other": "",
            "antibiotics": NO,
            "antibiotics_date": None,
            "antibiotics_given": Antibiotics.objects.none(),
            "antibiotics_given_other": "",
            "other_drugs": NO,
            "other_drugs_date": None,
            "other_drugs_given": Drugs.objects.none(),
            "other_drugs_given_other": "",
        }

    def test_form_validator_allows_valid_in_person_visit(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_cm_confirmed_na_if_lp_not_completed(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "lp_completed": NO,
                "cm_confirmed": NO,
            }
        )
        self.assertFormValidatorError(
            field="cm_confirmed",
            expected_msg="This field is not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_confirmed_applicable_if_lp_completed(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="cm_confirmed",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_tx_na_if_cm_not_confirmed(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": NO,
                "cm_tx": NO,
            }
        )
        self.assertFormValidatorError(
            field="cm_tx",
            expected_msg="This field is not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_tx_applicable_if_cm_confirmed(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "cm_tx": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="cm_tx",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_tx_given_na_if_cm_tx_no(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "cm_tx": NO,
                "cm_tx_given": "1w_amb_5fc",
            }
        )
        self.assertFormValidatorError(
            field="cm_tx_given",
            expected_msg="This field is not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_tx_given_applicable_if_cm_tx(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "cm_tx": YES,
                "cm_tx_given": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="cm_tx_given",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_tx_given_other_required_if_specified(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "cm_tx": YES,
                "cm_tx_given": OTHER,
                "cm_tx_given_other": "",
            }
        )
        self.assertFormValidatorError(
            field="cm_tx_given_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_tx_given_other_not_required_if_not_specified(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "cm_tx": YES,
                "cm_tx_given": "1w_amb_5fc",
                "cm_tx_given_other": "some_other_cm_tx_given",
            }
        )
        self.assertFormValidatorError(
            field="cm_tx_given_other",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    # tb_tx validation tests
    def test_tb_tx_given_other_required_if_specified(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "tb_tx_given": TbTreatments.objects.filter(name=OTHER),
                "tb_tx_given_other": "",
            }
        )
        self.assertFormValidatorError(
            field="tb_tx_given_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_tb_tx_given_other_not_required_if_not_specified(self):
        tb_treatments = [
            tx[0] for tx in list_data["effect_lists.tbtreatments"] if tx[0] != OTHER
        ]

        for tb_tx in tb_treatments:
            with self.subTest(tb_tx=tb_tx):
                cleaned_data = deepcopy(self.get_cleaned_data_patient_no_cm_no_tx())
                cleaned_data.update(
                    {
                        "tb_tx_given": TbTreatments.objects.filter(name=tb_tx),
                        "tb_tx_given_other": "some_other_tb_tx",
                    }
                )
                self.assertFormValidatorError(
                    field="tb_tx_given_other",
                    expected_msg="This field is not required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    # steroid validation tests
    def test_steroids_given_na_if_steroids_no(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "steroids": NO,
                "steroids_given": "oral_prednisolone",
                "steroids_given_other": "",
                "steroids_course": 1,
            }
        )
        self.assertFormValidatorError(
            field="steroids_given",
            expected_msg="This field is not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_steroids_given_applicable_if_steroids(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "steroids": YES,
                "steroids_given": NOT_APPLICABLE,
                "steroids_given_other": "",
                "steroids_course": None,
            }
        )
        self.assertFormValidatorError(
            field="steroids_given",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_steroids_given_other_required_if_specified(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "steroids": YES,
                "steroids_given": OTHER,
                "steroids_given_other": "",
                "steroids_course": 1,
            }
        )
        self.assertFormValidatorError(
            field="steroids_given_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_steroids_given_other_not_required_if_not_specified(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "steroids": YES,
                "steroids_given": "oral_prednisolone",
                "steroids_given_other": "xxx",
                "steroids_course": 1,
            }
        )
        self.assertFormValidatorError(
            field="steroids_given_other",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_steroids_course_not_required_if_steroids_no(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "steroids": NO,
                "steroids_given": NOT_APPLICABLE,
                "steroids_given_other": "",
                "steroids_course": 1,
            }
        )
        self.assertFormValidatorError(
            field="steroids_course",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_steroids_course_required_if_steroids(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "steroids": YES,
                "steroids_given": "oral_prednisolone",
                "steroids_given_other": "",
                "steroids_course": None,
            }
        )
        self.assertFormValidatorError(
            field="steroids_course",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    # antibiotic validation tests
    def test_antibiotics_other_required_if_specified(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        cleaned_data.update(
            {
                "antibiotics_given": Antibiotics.objects.filter(name=OTHER),
                "antibiotics_given_other": "",
            }
        )
        self.assertFormValidatorError(
            field="antibiotics_given_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_antibiotics_other_not_required_if_not_specified(self):
        antibiotic_choices = [
            ab[0] for ab in list_data["effect_lists.antibiotics"] if ab[0] != OTHER
        ]
        for antibiotic in antibiotic_choices:
            with self.subTest(antibiotic=antibiotic):
                cleaned_data = deepcopy(self.get_cleaned_data_patient_no_cm_no_tx())
                cleaned_data.update(
                    {
                        "antibiotics_given": Antibiotics.objects.filter(
                            name=antibiotic
                        ),
                        "antibiotics_given_other": "some_other_antibiotics",
                    }
                )
                self.assertFormValidatorError(
                    field="antibiotics_given_other",
                    expected_msg="This field is not required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )
