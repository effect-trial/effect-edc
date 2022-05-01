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

    def get_cleaned_data_patient_with_cm_with_all_tx(self):
        return {
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "lp_completed": YES,
            "cm_confirmed": YES,
            "cm_tx": YES,
            "cm_tx_given": "1w_amb_5fc",
            "cm_tx_given_other": "",
            "tb_tx": YES,
            "tb_tx_date": self.get_utcnow_as_date(),
            "tb_tx_given": TbTreatments.objects.filter(name="H"),
            "tb_tx_given_other": "",
            "tb_tx_reason_no": NOT_APPLICABLE,
            "tb_tx_reason_no_other": "",
            "steroids": YES,
            "steroids_date": self.get_utcnow_as_date(),
            "steroids_given": "oral_prednisolone",
            "steroids_given_other": "",
            "steroids_course": 3,
            "co_trimoxazole": YES,
            "co_trimoxazole_date": self.get_utcnow_as_date(),
            "co_trimoxazole_reason_no": NOT_APPLICABLE,
            "co_trimoxazole_reason_no_other": "",
            "antibiotics": YES,
            "antibiotics_date": self.get_utcnow_as_date(),
            "antibiotics_given": Antibiotics.objects.filter(name="amoxicillin"),
            "antibiotics_given_other": "",
            "other_drugs": YES,
            "other_drugs_date": self.get_utcnow_as_date(),
            "other_drugs_given": Drugs.objects.filter(name="vitamins"),
            "other_drugs_given_other": "",
        }

    def test_cleaned_data_patient_no_cm_no_tx_ok(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_cleaned_data_patient_with_cm_with_all_tx_ok(self):
        cleaned_data = self.get_cleaned_data_patient_with_cm_with_all_tx()
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
                "steroids_date": self.get_utcnow_as_date(),
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
                "steroids_date": self.get_utcnow_as_date(),
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
                "steroids_date": self.get_utcnow_as_date(),
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
                "steroids_date": self.get_utcnow_as_date(),
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

    def test_date_fields_required_if_prescribed_yes(self):
        for field in [
            "tb_tx",
            "steroids",
            "co_trimoxazole",
            "antibiotics",
            "other_drugs",
        ]:
            with self.subTest(field=field):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
                cleaned_data.update(
                    {
                        field: YES,
                        f"{field}_date": None,
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field}_date",
                    expected_msg="This field is required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_date_fields_not_required_if_prescribed_no(self):
        for field in [
            "tb_tx",
            "steroids",
            "co_trimoxazole",
            "antibiotics",
            "other_drugs",
        ]:
            with self.subTest(field=field):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
                cleaned_data.update(
                    {
                        field: NO,
                        f"{field}_date": self.get_utcnow_as_date(),
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field}_date",
                    expected_msg="This field is not required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_m2m_fields_required_if_prescribed_yes(self):
        for m2m_field, list_model in [
            ("tb_tx", TbTreatments),
            ("antibiotics", Antibiotics),
            ("other_drugs", Drugs),
        ]:
            with self.subTest(m2m_field=m2m_field, list_model=list_model):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
                cleaned_data.update(
                    {
                        m2m_field: YES,
                        f"{m2m_field}_date": self.get_utcnow_as_date(),
                        f"{m2m_field}_given": list_model.objects.none(),
                    }
                )
                self.assertFormValidatorError(
                    field=f"{m2m_field}_given",
                    expected_msg="This field is required",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_m2m_fields_not_applicable_if_prescribed_no(self):
        for m2m_field, list_model in [
            ("tb_tx", TbTreatments),
            ("antibiotics", Antibiotics),
            ("other_drugs", Drugs),
        ]:
            with self.subTest(m2m_field=m2m_field, list_model=list_model):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
                cleaned_data.update(
                    {
                        m2m_field: NO,
                        f"{m2m_field}_date": None,
                        f"{m2m_field}_given": list_model.objects.all(),
                    }
                )
                self.assertFormValidatorError(
                    field=f"{m2m_field}_given",
                    expected_msg="This field is not required",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_m2m_other_fields_required_if_other_specified(self):
        for m2m_field, list_model in [
            ("tb_tx", TbTreatments),
            ("antibiotics", Antibiotics),
            ("other_drugs", Drugs),
        ]:
            with self.subTest(m2m_field=m2m_field, list_model=list_model):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
                cleaned_data.update(
                    {
                        m2m_field: YES,
                        f"{m2m_field}_date": self.get_utcnow_as_date(),
                        f"{m2m_field}_given": list_model.objects.filter(name=OTHER),
                        f"{m2m_field}_given_other": "",
                    }
                )
                if m2m_field == "tb_tx":
                    cleaned_data.update({"tb_tx_reason_no": NOT_APPLICABLE})
                self.assertFormValidatorError(
                    field=f"{m2m_field}_given_other",
                    expected_msg="This field is required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

                cleaned_data.update({f"{m2m_field}_given_other": "Some other value"})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_m2m_other_fields_not_required_if_not_specified(self):
        for m2m_field, list_model in [
            ("tb_tx", TbTreatments),
            ("antibiotics", Antibiotics),
            ("other_drugs", Drugs),
        ]:
            with self.subTest(m2m_field=m2m_field, list_model=list_model):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
                cleaned_data.update(
                    {
                        m2m_field: NO,
                        f"{m2m_field}_date": None,
                        f"{m2m_field}_given": list_model.objects.none(),
                        f"{m2m_field}_given_other": "Some other value",
                    }
                )
                self.assertFormValidatorError(
                    field=f"{m2m_field}_given_other",
                    expected_msg="This field is not required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

                cleaned_data.update({f"{m2m_field}_given_other": ""})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_reason_no_applicable_if_prescribed_no(self):
        for field in ["tb_tx", "co_trimoxazole"]:
            with self.subTest(field=field):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
                cleaned_data.update({f"{field}_reason_no": NOT_APPLICABLE})
                self.assertFormValidatorError(
                    field=f"{field}_reason_no",
                    expected_msg="This field is applicable",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_reason_no_not_applicable_if_prescribed_yes(self):
        for field in ["tb_tx", "co_trimoxazole"]:
            with self.subTest(field=field):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
                cleaned_data.update(
                    {
                        field: YES,
                        f"{field}_date": self.get_utcnow_as_date(),
                        f"{field}_reason_no": "contraindicated",
                    }
                )
                if field == "tb_tx":
                    cleaned_data.update(
                        {"tb_tx_given": TbTreatments.objects.filter(name="H")}
                    )

                self.assertFormValidatorError(
                    field=f"{field}_reason_no",
                    expected_msg="This field is not applicable",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_reason_no_other_required_if_specified(self):
        for field in ["tb_tx", "co_trimoxazole"]:
            with self.subTest(field=field):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
                cleaned_data.update(
                    {
                        field: NO,
                        f"{field}_reason_no": OTHER,
                        f"{field}_reason_no_other": "",
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field}_reason_no_other",
                    expected_msg="This field is required",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_reason_no_other_not_required_if_not_specified(self):
        for field in ["tb_tx", "co_trimoxazole"]:
            with self.subTest(field=field):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx()
                cleaned_data.update(
                    {
                        field: NO,
                        f"{field}_reason_no": "contraindicated",
                        f"{field}_reason_no_other": "Some other reason",
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field}_reason_no_other",
                    expected_msg="This field is not required",
                    form_validator=self.validate_form_validator(cleaned_data),
                )
