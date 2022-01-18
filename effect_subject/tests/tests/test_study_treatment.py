from copy import deepcopy

from django.test import TestCase
from edc_constants.constants import NO, NOT_APPLICABLE, OTHER, YES
from model_bakery import baker

from effect_lists.list_data import list_data
from effect_lists.models import Antibiotics, TbTreatments
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms import StudyTreatmentForm
from effect_subject.forms.study_treatment_form import StudyTreatmentFormValidator


class TestFollowup(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def test_ok(self):
        subject_visit = self.subject_visit
        obj = baker.make_recipe(
            "effect_subject.studytreatment", subject_visit=subject_visit
        )
        form = StudyTreatmentForm(instance=obj)
        form.is_valid()


class TestFollowupFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = StudyTreatmentFormValidator

    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def get_valid_non_cm_patient_without_treatment_data(self):
        return {
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "lp_completed": NO,
            "cm_confirmed": NOT_APPLICABLE,
            "cm_tx_administered": NOT_APPLICABLE,
            "cm_tx_given": NOT_APPLICABLE,
            "cm_tx_given_other": "",
            "tb_tx_given": TbTreatments.objects.none(),
            "tb_tx_given_other": "",
            "steroids_administered": NO,
            "which_steroids": NOT_APPLICABLE,
            "which_steroids_other": "",
            "steroids_course_duration": None,
            "co_trimoxazole": NO,
            "antibiotics": Antibiotics.objects.none(),
            "antibiotics_other": "",
        }

    def test_form_validator_allows_valid_in_person_visit(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertDictEqual({}, form_validator._errors)

    def test_cm_confirmed_na_if_lp_not_completed(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "lp_completed": NO,
                "cm_confirmed": NO,
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="cm_confirmed",
            expected_msg="This field is not applicable.",
        )

    def test_cm_confirmed_applicable_if_lp_completed(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": NOT_APPLICABLE,
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="cm_confirmed",
            expected_msg="This field is applicable.",
        )

    def test_cm_tx_administered_na_if_cm_not_confirmed(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": NO,
                "cm_tx_administered": NO,
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="cm_tx_administered",
            expected_msg="This field is not applicable.",
        )

    def test_cm_tx_administered_applicable_if_cm_confirmed(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "cm_tx_administered": NOT_APPLICABLE,
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="cm_tx_administered",
            expected_msg="This field is applicable.",
        )

    def test_cm_tx_given_na_if_cm_tx_not_administered(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "cm_tx_administered": NO,
                "cm_tx_given": "1w_amb_5fc",
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="cm_tx_given",
            expected_msg="This field is not applicable.",
        )

    def test_cm_tx_given_applicable_if_cm_tx_administered(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "cm_tx_administered": YES,
                "cm_tx_given": NOT_APPLICABLE,
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="cm_tx_given",
            expected_msg="This field is applicable.",
        )

    def test_cm_tx_given_other_required_if_specified(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "cm_tx_administered": YES,
                "cm_tx_given": OTHER,
                "cm_tx_given_other": "",
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="cm_tx_given_other",
            expected_msg="This field is required.",
        )

    def test_cm_tx_given_other_not_required_if_not_specified(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "cm_tx_administered": YES,
                "cm_tx_given": "1w_amb_5fc",
                "cm_tx_given_other": "some_other_cm_tx_given",
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="cm_tx_given_other",
            expected_msg="This field is not required.",
        )

    # tb_tx validation tests
    def test_tb_tx_given_other_required_if_specified(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "tb_tx_given": TbTreatments.objects.filter(name=OTHER),
                "tb_tx_given_other": "",
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="tb_tx_given_other",
            expected_msg="This field is required.",
        )

    def test_tb_tx_given_other_not_required_if_not_specified(self):
        tb_treatments = [
            tx[0] for tx in list_data["effect_lists.tbtreatments"] if tx[0] != OTHER
        ]

        for tb_tx in tb_treatments:
            with self.subTest(tb_tx=tb_tx):
                cleaned_data = deepcopy(
                    self.get_valid_non_cm_patient_without_treatment_data()
                )
                cleaned_data.update(
                    {
                        "tb_tx_given": TbTreatments.objects.filter(name=tb_tx),
                        "tb_tx_given_other": "some_other_tb_tx",
                    }
                )
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertFieldFormValidationErrorRaised(
                    form_validator=form_validator,
                    field="tb_tx_given_other",
                    expected_msg="This field is not required.",
                )

    # steroid validation tests
    def test_which_steroids_na_if_steroids_not_administered(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "steroids_administered": NO,
                "which_steroids": "oral_prednisolone",
                "which_steroids_other": "",
                "steroids_course_duration": 1,
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="which_steroids",
            expected_msg="This field is not applicable.",
        )

    def test_which_steroids_applicable_if_steroids_administered(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "steroids_administered": YES,
                "which_steroids": NOT_APPLICABLE,
                "which_steroids_other": "",
                "steroids_course_duration": None,
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="which_steroids",
            expected_msg="This field is applicable.",
        )

    def test_which_steroids_other_required_if_specified(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "steroids_administered": YES,
                "which_steroids": OTHER,
                "which_steroids_other": "",
                "steroids_course_duration": 1,
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="which_steroids_other",
            expected_msg="This field is required.",
        )

    def test_which_steroids_other_not_required_if_not_specified(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "steroids_administered": YES,
                "which_steroids": "oral_prednisolone",
                "which_steroids_other": "xxx",
                "steroids_course_duration": 1,
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="which_steroids_other",
            expected_msg="This field is not required.",
        )

    def test_steroids_course_duration_not_required_if_steroids_not_administered(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "steroids_administered": NO,
                "which_steroids": NOT_APPLICABLE,
                "which_steroids_other": "",
                "steroids_course_duration": 1,
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="steroids_course_duration",
            expected_msg="This field is not required.",
        )

    def test_steroids_course_duration_required_if_steroids_administered(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "steroids_administered": YES,
                "which_steroids": "oral_prednisolone",
                "which_steroids_other": "",
                "steroids_course_duration": None,
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="steroids_course_duration",
            expected_msg="This field is required.",
        )

    # antibiotic validation tests
    def test_antibiotics_other_required_if_specified(self):
        cleaned_data = self.get_valid_non_cm_patient_without_treatment_data()
        cleaned_data.update(
            {
                "antibiotics": Antibiotics.objects.filter(name=OTHER),
                "antibiotics_other": "",
            }
        )
        form_validator = self.validate_form_validator(cleaned_data)
        self.assertFieldFormValidationErrorRaised(
            form_validator=form_validator,
            field="antibiotics_other",
            expected_msg="This field is required.",
        )

    def test_antibiotics_other_not_required_if_not_specified(self):
        antibiotic_choices = [
            ab[0] for ab in list_data["effect_lists.antibiotics"] if ab[0] != OTHER
        ]
        for antibiotic in antibiotic_choices:
            with self.subTest(antibiotic=antibiotic):
                cleaned_data = deepcopy(
                    self.get_valid_non_cm_patient_without_treatment_data()
                )
                cleaned_data.update(
                    {
                        "antibiotics": Antibiotics.objects.filter(name=antibiotic),
                        "antibiotics_other": "some_other_antibiotics",
                    }
                )
                form_validator = self.validate_form_validator(cleaned_data)
                self.assertFieldFormValidationErrorRaised(
                    form_validator=form_validator,
                    field="antibiotics_other",
                    expected_msg="This field is not required.",
                )
