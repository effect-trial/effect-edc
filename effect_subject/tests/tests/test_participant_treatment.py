from typing import Optional

from django.test import TestCase
from edc_constants.constants import NO, NOT_APPLICABLE, NOT_ESTIMATED, OTHER, YES
from edc_test_utils.validate_fields_exists_or_raise import (
    validate_fields_exists_or_raise,
)
from edc_utils import get_utcnow_as_date
from edc_visit_schedule.constants import DAY01
from model_bakery import baker

from effect_lists.models import Antibiotics, Drugs, TbTreatments
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms import ParticipantTreatmentForm
from effect_subject.forms.participant_treatment_form import (
    ParticipantTreatmentFormValidator,
)
from effect_subject.models import ParticipantTreatment, SubjectVisit


class TestParticipantTreatment(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.get_subject_visit()

    def test_ok(self):
        subject_visit = self.get_next_subject_visit(self.subject_visit)  # d3
        subject_visit = self.get_next_subject_visit(subject_visit)  # d9
        subject_visit = self.get_next_subject_visit(subject_visit)  # d14
        obj = baker.make_recipe(
            "effect_subject.participanttreatment", subject_visit=subject_visit
        )
        form = ParticipantTreatmentForm(instance=obj)
        form.is_valid()


class TestParticipantTreatmentFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_cls = ParticipantTreatmentFormValidator
    form_validator_model_cls = ParticipantTreatment

    def setUp(self) -> None:
        super().setUp()
        subject_visit = self.get_subject_visit()
        subject_visit = self.get_next_subject_visit(subject_visit)
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.get_next_subject_visit(subject_visit)

    @staticmethod
    def get_cleaned_data_patient_no_cm_no_tx(visit_code: Optional[str] = None):
        visit_code = visit_code or DAY01
        subject_visit = SubjectVisit.objects.get(visit_code=visit_code)
        cleaned_data = {
            "subject_visit": subject_visit,
            "report_datetime": subject_visit.report_datetime,
            "lp_completed": NO,
            "cm_confirmed": NOT_APPLICABLE,
            "on_cm_tx": NOT_APPLICABLE,
            "cm_tx_given": NOT_APPLICABLE,
            "cm_tx_given_other": "",
            "on_tb_tx": NO,
            "tb_tx_date": None,
            "tb_tx_date_estimated": NOT_APPLICABLE,
            "tb_tx_given": TbTreatments.objects.none(),
            "tb_tx_given_other": "",
            "tb_tx_reason_no": "contraindicated",
            "tb_tx_reason_no_other": "",
            "on_steroids": NO,
            "steroids_date": None,
            "steroids_date_estimated": NOT_APPLICABLE,
            "steroids_given": NOT_APPLICABLE,
            "steroids_given_other": "",
            "steroids_course": None,
            "on_co_trimoxazole": NO,
            "co_trimoxazole_date": None,
            "co_trimoxazole_date_estimated": NOT_APPLICABLE,
            "co_trimoxazole_reason_no": "deferred_local_clinic",
            "co_trimoxazole_reason_no_other": "",
            "on_antibiotics": NO,
            "antibiotics_date": None,
            "antibiotics_date_estimated": NOT_APPLICABLE,
            "antibiotics_given": Antibiotics.objects.none(),
            "antibiotics_given_other": "",
            "on_other_drugs": NO,
            "other_drugs_date": None,
            "other_drugs_date_estimated": NOT_APPLICABLE,
            "other_drugs_given": Drugs.objects.none(),
            "other_drugs_given_other": "",
        }

        validate_fields_exists_or_raise(cleaned_data, ParticipantTreatment)

        return cleaned_data

    @staticmethod
    def get_cleaned_data_patient_with_cm_with_all_tx(visit_code: Optional[str] = None):
        visit_code = visit_code or DAY01
        subject_visit = SubjectVisit.objects.get(visit_code=visit_code)
        cleaned_data = {
            "subject_visit": subject_visit,
            "report_datetime": subject_visit.report_datetime,
            "lp_completed": YES,
            "cm_confirmed": YES,
            "on_cm_tx": YES,
            "cm_tx_given": "1w_amb_5fc",
            "cm_tx_given_other": "",
            "on_tb_tx": YES,
            "tb_tx_date": get_utcnow_as_date(),
            "tb_tx_date_estimated": NOT_ESTIMATED,
            "tb_tx_given": TbTreatments.objects.filter(name="H"),
            "tb_tx_given_other": "",
            "tb_tx_reason_no": NOT_APPLICABLE,
            "tb_tx_reason_no_other": "",
            "on_steroids": YES,
            "steroids_date": get_utcnow_as_date(),
            "steroids_date_estimated": NOT_ESTIMATED,
            "steroids_given": "oral_prednisolone",
            "steroids_given_other": "",
            "steroids_course": 3,
            "on_co_trimoxazole": YES,
            "co_trimoxazole_date": get_utcnow_as_date(),
            "co_trimoxazole_date_estimated": NOT_ESTIMATED,
            "co_trimoxazole_reason_no": NOT_APPLICABLE,
            "co_trimoxazole_reason_no_other": "",
            "on_antibiotics": YES,
            "antibiotics_date": get_utcnow_as_date(),
            "antibiotics_date_estimated": NOT_ESTIMATED,
            "antibiotics_given": Antibiotics.objects.filter(name="amoxicillin"),
            "antibiotics_given_other": "",
            "on_other_drugs": YES,
            "other_drugs_date": get_utcnow_as_date(),
            "other_drugs_date_estimated": NOT_ESTIMATED,
            "other_drugs_given": Drugs.objects.filter(name="vitamins"),
            "other_drugs_given_other": "",
        }

        validate_fields_exists_or_raise(cleaned_data, ParticipantTreatment)

        return cleaned_data

    def test_cleaned_data_patient_no_cm_no_tx_ok(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_cleaned_data_patient_with_cm_with_all_tx_ok(self):
        cleaned_data = self.get_cleaned_data_patient_with_cm_with_all_tx(visit_code=DAY01)
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_cm_confirmed_na_if_lp_not_completed(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
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
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
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
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": NO,
                "on_cm_tx": NO,
            }
        )
        self.assertFormValidatorError(
            field="on_cm_tx",
            expected_msg="This field is not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_tx_applicable_if_cm_confirmed(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "on_cm_tx": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="on_cm_tx",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_tx_given_na_if_cm_tx_no(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "on_cm_tx": NO,
                "cm_tx_given": "1w_amb_5fc",
            }
        )
        self.assertFormValidatorError(
            field="cm_tx_given",
            expected_msg="This field is not applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_tx_given_applicable_if_cm_tx(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "on_cm_tx": YES,
                "cm_tx_given": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="cm_tx_given",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_tx_given_other_required_if_specified(self):
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "on_cm_tx": YES,
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
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "lp_completed": YES,
                "cm_confirmed": YES,
                "on_cm_tx": YES,
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
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "on_steroids": NO,
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
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "on_steroids": YES,
                "steroids_date": get_utcnow_as_date(),
                "steroids_date_estimated": "MD",
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
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "on_steroids": YES,
                "steroids_date": get_utcnow_as_date(),
                "steroids_date_estimated": "MD",
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
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "on_steroids": YES,
                "steroids_date": get_utcnow_as_date(),
                "steroids_date_estimated": "MD",
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
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "on_steroids": NO,
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
        cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
        cleaned_data.update(
            {
                "on_steroids": YES,
                "steroids_date": get_utcnow_as_date(),
                "steroids_date_estimated": "MD",
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
        for field_stub in [
            "tb_tx",
            "steroids",
            "co_trimoxazole",
            "antibiotics",
            "other_drugs",
        ]:
            with self.subTest(field_stub=field_stub):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update(
                    {
                        f"on_{field_stub}": YES,
                        f"{field_stub}_date": None,
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field_stub}_date",
                    expected_msg="This field is required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_date_fields_not_required_if_prescribed_no(self):
        for field_stub in [
            "tb_tx",
            "steroids",
            "co_trimoxazole",
            "antibiotics",
            "other_drugs",
        ]:
            with self.subTest(field_stub=field_stub):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update(
                    {
                        f"on_{field_stub}": NO,
                        f"{field_stub}_date": get_utcnow_as_date(),
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field_stub}_date",
                    expected_msg="This field is not required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_date_estimated_fields_applicable_if_prescribed_yes(self):
        for field_stub in [
            "tb_tx",
            "steroids",
            "co_trimoxazole",
            "antibiotics",
            "other_drugs",
        ]:
            with self.subTest(field_stub=field_stub):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update(
                    {
                        f"on_{field_stub}": YES,
                        f"{field_stub}_date": get_utcnow_as_date(),
                        f"{field_stub}_date_estimated": NOT_APPLICABLE,
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field_stub}_date_estimated",
                    expected_msg="This field is applicable",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_date_estimated_fields_not_applicable_if_prescribed_no(self):
        for field_stub in [
            "tb_tx",
            "steroids",
            "co_trimoxazole",
            "antibiotics",
            "other_drugs",
        ]:
            with self.subTest(field_stub=field_stub):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update(
                    {
                        f"on_{field_stub}": NO,
                        f"{field_stub}_date": None,
                        f"{field_stub}_date_estimated": "YMD",
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field_stub}_date_estimated",
                    expected_msg="This field is not applicable.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_m2m_fields_required_if_prescribed_yes(self):
        for field_stub, list_model in [
            ("tb_tx", TbTreatments),
            ("antibiotics", Antibiotics),
            ("other_drugs", Drugs),
        ]:
            with self.subTest(field_stub=field_stub, list_model=list_model):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update(
                    {
                        f"on_{field_stub}": YES,
                        f"{field_stub}_date": get_utcnow_as_date(),
                        f"{field_stub}_date_estimated": "YMD",
                        f"{field_stub}_given": list_model.objects.none(),
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field_stub}_given",
                    expected_msg="This field is required",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_m2m_fields_not_applicable_if_prescribed_no(self):
        for field_stub, list_model in [
            ("tb_tx", TbTreatments),
            ("antibiotics", Antibiotics),
            ("other_drugs", Drugs),
        ]:
            with self.subTest(field_stub=field_stub, list_model=list_model):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update(
                    {
                        f"on_{field_stub}": NO,
                        f"{field_stub}_date": None,
                        f"{field_stub}_given": list_model.objects.all(),
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field_stub}_given",
                    expected_msg="This field is not required",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_m2m_other_fields_required_if_other_specified(self):
        for field_stub, list_model in [
            ("tb_tx", TbTreatments),
            ("antibiotics", Antibiotics),
            ("other_drugs", Drugs),
        ]:
            with self.subTest(field_stub=field_stub, list_model=list_model):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update(
                    {
                        f"on_{field_stub}": YES,
                        f"{field_stub}_date": get_utcnow_as_date(),
                        f"{field_stub}_date_estimated": "YMD",
                        f"{field_stub}_given": list_model.objects.filter(name=OTHER),
                        f"{field_stub}_given_other": "",
                    }
                )
                if field_stub == "tb_tx":
                    cleaned_data.update({"tb_tx_reason_no": NOT_APPLICABLE})
                self.assertFormValidatorError(
                    field=f"{field_stub}_given_other",
                    expected_msg="This field is required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

                cleaned_data.update({f"{field_stub}_given_other": "Some other value"})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_m2m_other_fields_not_required_if_not_specified(self):
        for field_stub, list_model in [
            ("tb_tx", TbTreatments),
            ("antibiotics", Antibiotics),
            ("other_drugs", Drugs),
        ]:
            with self.subTest(field_stub=field_stub, list_model=list_model):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update(
                    {
                        f"on_{field_stub}": NO,
                        f"{field_stub}_date": None,
                        f"{field_stub}_given": list_model.objects.none(),
                        f"{field_stub}_given_other": "Some other value",
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field_stub}_given_other",
                    expected_msg="This field is not required.",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

                cleaned_data.update({f"{field_stub}_given_other": ""})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_reason_no_applicable_if_prescribed_no(self):
        for field_stub in ["tb_tx", "co_trimoxazole"]:
            with self.subTest(field_stub=field_stub):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update({f"{field_stub}_reason_no": NOT_APPLICABLE})
                self.assertFormValidatorError(
                    field=f"{field_stub}_reason_no",
                    expected_msg="This field is applicable",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_reason_no_not_applicable_if_prescribed_yes(self):
        for field_stub in ["tb_tx", "co_trimoxazole"]:
            with self.subTest(field_stub=field_stub):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update(
                    {
                        f"on_{field_stub}": YES,
                        f"{field_stub}_date": get_utcnow_as_date(),
                        f"{field_stub}_date_estimated": "YMD",
                        f"{field_stub}_reason_no": "contraindicated",
                    }
                )
                if field_stub == "tb_tx":
                    cleaned_data.update({"tb_tx_given": TbTreatments.objects.filter(name="H")})

                self.assertFormValidatorError(
                    field=f"{field_stub}_reason_no",
                    expected_msg="This field is not applicable",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_reason_no_other_required_if_specified(self):
        for field_stub in ["tb_tx", "co_trimoxazole"]:
            with self.subTest(field_stub=field_stub):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update(
                    {
                        f"on_{field_stub}": NO,
                        f"{field_stub}_reason_no": OTHER,
                        f"{field_stub}_reason_no_other": "",
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field_stub}_reason_no_other",
                    expected_msg="This field is required",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_reason_no_other_not_required_if_not_specified(self):
        for field_stub in ["tb_tx", "co_trimoxazole"]:
            with self.subTest(field_stub=field_stub):
                cleaned_data = self.get_cleaned_data_patient_no_cm_no_tx(visit_code=DAY01)
                cleaned_data.update(
                    {
                        f"on_{field_stub}": NO,
                        f"{field_stub}_reason_no": "contraindicated",
                        f"{field_stub}_reason_no_other": "Some other reason",
                    }
                )
                self.assertFormValidatorError(
                    field=f"{field_stub}_reason_no_other",
                    expected_msg="This field is not required",
                    form_validator=self.validate_form_validator(cleaned_data),
                )
