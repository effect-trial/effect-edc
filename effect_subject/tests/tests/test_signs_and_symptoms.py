from copy import deepcopy

from django.db.models import Q
from django.test import TestCase, tag
from edc_constants.constants import NO, NONE, NOT_APPLICABLE, OTHER, UNKNOWN, YES
from model_bakery import baker

from effect_lists.models import BloodTests, SiSx
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

    def get_valid_patient_with_no_signs_or_symptoms(self):
        return {
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "any_sx": NO,
            "current_sx": SiSx.objects.filter(name=NONE),
            "current_sx_other": "",
            "current_sx_gte_g3": SiSx.objects.filter(name=NONE),
            "current_sx_gte_g3_other": "",
            "headache_duration": "",
            "visual_field_loss": "",
            "reportable_as_ae": NOT_APPLICABLE,
            "patient_admitted": NOT_APPLICABLE,
            "cm_sx": NOT_APPLICABLE,
            "cm_sx_lp_done": NOT_APPLICABLE,
            "cm_sx_bloods_take": BloodTests.objects.filter(name=NOT_APPLICABLE),
            "cm_sx_bloods_taken_other": "",
            "cm_sx_patient_admitted": NOT_APPLICABLE,
        }

    def get_valid_patient_any_sx_unknown(self):
        cleaned_data = deepcopy(self.get_valid_patient_with_no_signs_or_symptoms())
        cleaned_data.update(
            {
                "any_sx": UNKNOWN,
                "current_sx": SiSx.objects.filter(name=NOT_APPLICABLE),
                "current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE),
            }
        )
        return cleaned_data

    def get_valid_patient_with_signs_or_symptoms(self):
        return {
            "appointment": self.subject_visit.appointment,
            "report_datetime": self.subject_visit.report_datetime,
            "any_sx": YES,
            "current_sx": SiSx.objects.filter(Q(name="fever") | Q(name="vomiting")),
            "current_sx_other": "",
            "current_sx_gte_g3": SiSx.objects.filter(name=NONE),
            "current_sx_gte_g3_other": "",
            "headache_duration": "",
            "visual_field_loss": "",
            "reportable_as_ae": NO,
            "patient_admitted": NO,
            "cm_sx": NO,
            "cm_sx_lp_done": NOT_APPLICABLE,
            "cm_sx_bloods_taken": BloodTests.objects.filter(name=NOT_APPLICABLE),
            "cm_sx_bloods_taken_other": "",
            "cm_sx_patient_admitted": NOT_APPLICABLE,
        }

    def get_valid_patient_with_g3_signs_or_symptoms(self):
        cleaned_data = deepcopy(self.get_valid_patient_with_signs_or_symptoms())
        cleaned_data.update(
            {
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
                "current_sx_gte_g3_other": "",
                "reportable_as_ae": YES,
            }
        )
        return cleaned_data

    def get_valid_patient_with_cm_symptoms(self):
        cleaned_data = deepcopy(self.get_valid_patient_with_g3_signs_or_symptoms())
        cleaned_data.update(
            {
                "cm_sx": YES,
                "cm_sx_lp_done": YES,
                "cm_sx_bloods_taken": BloodTests.objects.filter(
                    Q(name="chemistry") | Q(name="hematology")
                ),
                "cm_sx_bloods_taken_other": "",
                "cm_sx_patient_admitted": YES,
            }
        )
        return cleaned_data

    @staticmethod
    def get_non_yes_sx_selection(any_sx_answer: str):
        return (
            SiSx.objects.filter(name=NONE)
            if any_sx_answer == NO
            else SiSx.objects.filter(name=NOT_APPLICABLE)
        )

    def test_non_symptomatic_patient_valid(self):
        cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_any_sx_unknown_valid(self):
        cleaned_data = self.get_valid_patient_any_sx_unknown()
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

    def test_valid_patient_with_cm_symptoms(self):
        cleaned_data = self.get_valid_patient_with_cm_symptoms()
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_m2m_sx_selections_expect_none_if_any_sx_is_no(self):
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
            expected_msg="Expected '--No symptoms to report' only.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(name=NONE),
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3",
            expected_msg="Expected '--No symptoms to report' only.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3": SiSx.objects.filter(name=NONE)})
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
            expected_msg="Expected '--Not applicable (if 'Unknown')' only.",
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
            expected_msg="Expected '--Not applicable (if 'Unknown')' only.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {"current_sx_gte_g3": SiSx.objects.filter(name=NOT_APPLICABLE)}
        )
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_m2m_current_sx_with_na_and_none_invalid_if_any_sx_is_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": YES,
                "current_sx": SiSx.objects.filter(
                    Q(name="fever") | Q(name=NONE) | Q(name=NOT_APPLICABLE)
                ),
            }
        )
        self.assertFormValidatorError(
            field="current_sx",
            expected_msg=(
                "Invalid selection. "
                "Cannot be any of: --No symptoms to report, --Not applicable (if 'Unknown')."
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(
                    Q(name="fever") | Q(name=NOT_APPLICABLE)
                ),
            }
        )
        self.assertFormValidatorError(
            field="current_sx",
            expected_msg=(
                "Invalid selection. Cannot be any of: --Not applicable (if 'Unknown')."
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx": SiSx.objects.filter(Q(name="fever"))})
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_m2m_current_sx_gte_g3_with_na_invalid_if_any_sx_is_yes(self):
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
                "Invalid selection. "
                "Cannot be any of: --Not applicable (if 'Unknown')."
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3": SiSx.objects.filter(Q(name="fever"))})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_m2m_current_sx_gte_g3_can_be_none_if_any_sx_is_yes(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": YES,
                "current_sx_gte_g3": SiSx.objects.filter(name=NONE),
                "reportable_as_ae": NO,
            }
        )
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

    def test_m2m_current_sx_gte_g3_cannot_be_none_with_another_selection(self):
        cleaned_data = self.get_valid_patient_with_g3_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": YES,
                "current_sx_gte_g3": SiSx.objects.filter(
                    Q(name="fever") | Q(name=NONE)
                ),
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3",
            expected_msg=(
                "Invalid combination. "
                "'--No symptoms to report' may not be combined with other selections"
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3": SiSx.objects.filter(Q(name="fever"))})
        self.assertFormValidatorNoError(self.validate_form_validator(cleaned_data))

        cleaned_data.update(
            {
                "current_sx_gte_g3": SiSx.objects.filter(Q(name=NONE)),
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
                "headache_duration": "2w",
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
                        else SiSx.objects.filter(name=NONE),
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
                    cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
                    cleaned_data.update(
                        {
                            "any_sx": any_sx_answer,
                            "current_sx": self.get_non_yes_sx_selection(any_sx_answer),
                            "current_sx_gte_g3": self.get_non_yes_sx_selection(
                                any_sx_answer
                            ),
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
                "current_sx_gte_g3": SiSx.objects.filter(name=NONE),
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

    def test_reportable_as_ae_yes_invalid_if_sx_gte_g3_none(self):
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

    def test_current_sx_gte_g3_not_required_if_any_sx_is_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update({"current_sx_gte_g3": SiSx.objects.filter(name=NONE)})

        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_sx_gte_g3_with_no_current_sx_raises_error(self):
        cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
        cleaned_data.update(
            {
                "any_sx": NO,
                "current_sx": SiSx.objects.filter(name=NONE),
                "current_sx_gte_g3": SiSx.objects.filter(name="fever"),
            }
        )
        self.assertFormValidatorError(
            field="current_sx_gte_g3",
            expected_msg="Expected '--No symptoms to report' only.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"current_sx_gte_g3": SiSx.objects.filter(name=NONE)})
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
                "current_sx_gte_g3": SiSx.objects.filter(
                    Q(name="fever") | Q(name="vomiting")
                ),
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

    def test_headache_duration_applicable_if_in_current_sx(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(name=HEADACHE),
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

    def test_headache_duration_not_applicable_if_not_in_current_sx(self):
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

    def test_visual_field_loss_applicable_if_in_current_sx(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "current_sx": SiSx.objects.filter(name=VISUAL_LOSS),
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

    def test_visual_field_loss_not_applicable_if_not_in_current_sx(self):
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
                    cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
                    cleaned_data.update(
                        {
                            "any_sx": any_sx_answer,
                            "current_sx": self.get_non_yes_sx_selection(any_sx_answer),
                            "current_sx_gte_g3": self.get_non_yes_sx_selection(
                                any_sx_answer
                            ),
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
                if answer == YES:
                    cleaned_data.update(
                        {
                            "cm_sx_lp_done": NO,
                            "cm_sx_bloods_taken": BloodTests.objects.filter(name=NONE),
                            "cm_sx_patient_admitted": NO,
                        }
                    )
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
                    cleaned_data = self.get_valid_patient_with_no_signs_or_symptoms()
                    cleaned_data.update(
                        {
                            "any_sx": any_sx_answer,
                            "current_sx": self.get_non_yes_sx_selection(any_sx_answer),
                            "current_sx_gte_g3": self.get_non_yes_sx_selection(
                                any_sx_answer
                            ),
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

    def test_cm_sx_lp_done_applicable_if_cm_sx_yes(self):
        cleaned_data = self.get_valid_patient_with_cm_symptoms()
        cleaned_data.update(
            {
                "cm_sx": YES,
                "cm_sx_lp_done": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="cm_sx_lp_done",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        for answer in [YES, NO]:
            with self.subTest(answer=answer):
                cleaned_data.update({"cm_sx_lp_done": answer})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_cm_sx_lp_done_not_applicable_if_cm_sx_not_yes(self):
        for cm_sx_answer in [NO, NOT_APPLICABLE]:
            for cm_sx_lp_done_answer in [YES, NO]:
                with self.subTest(
                    cm_sx_answer=cm_sx_answer,
                    cm_sx_lp_done_answer=cm_sx_lp_done_answer,
                ):
                    cleaned_data = (
                        self.get_valid_patient_with_signs_or_symptoms()
                        if cm_sx_answer == NO
                        else self.get_valid_patient_any_sx_unknown()
                    )
                    cleaned_data.update(
                        {
                            "cm_sx": cm_sx_answer,
                            "cm_sx_lp_done": cm_sx_lp_done_answer,
                        }
                    )
                    self.assertFormValidatorError(
                        field="cm_sx_lp_done",
                        expected_msg="This field is not applicable",
                        form_validator=self.validate_form_validator(cleaned_data),
                    )

                    cleaned_data.update({"cm_sx_lp_done": NOT_APPLICABLE})
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data)
                    )

    def test_cm_sx_bloods_taken_not_applicable_if_cm_sx_not_yes(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {"cm_sx_bloods_taken": BloodTests.objects.filter(name="chemistry")}
        )
        self.assertFormValidatorError(
            field="cm_sx_bloods_taken",
            expected_msg="This field is not applicable",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {"cm_sx_bloods_taken": BloodTests.objects.filter(name=NONE)}
        )
        self.assertFormValidatorError(
            field="cm_sx_bloods_taken",
            expected_msg="This field is not applicable",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {"cm_sx_bloods_taken": BloodTests.objects.filter(name=NOT_APPLICABLE)}
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_cm_sx_bloods_taken_applicable_if_cm_sx_is_yes(self):
        cleaned_data = self.get_valid_patient_with_cm_symptoms()
        cleaned_data.update(
            {"cm_sx_bloods_taken": BloodTests.objects.filter(name=NOT_APPLICABLE)}
        )
        self.assertFormValidatorError(
            field="cm_sx_bloods_taken",
            expected_msg="This field is applicable",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {"cm_sx_bloods_taken": BloodTests.objects.filter(name=NONE)}
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {"cm_sx_bloods_taken": BloodTests.objects.filter(name="chemistry")}
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_cm_sx_bloods_taken_allows_multiple_selections(self):
        cleaned_data = self.get_valid_patient_with_cm_symptoms()
        cleaned_data.update(
            {
                "cm_sx_bloods_taken": BloodTests.objects.filter(
                    Q(name="chemistry") | Q(name="hematology") | Q(name=OTHER)
                ),
                "cm_sx_bloods_taken_other": "Some other bloods...",
            }
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_cm_sx_bloods_taken_single_selection_only_for_none(self):
        cleaned_data = self.get_valid_patient_with_cm_symptoms()
        cleaned_data.update(
            {
                "cm_sx_bloods_taken": BloodTests.objects.filter(
                    Q(name=NONE) | Q(name="chemistry")
                )
            }
        )
        self.assertFormValidatorError(
            field="cm_sx_bloods_taken",
            expected_msg=(
                "Invalid combination. "
                "'--No bloods taken' may not be combined with other selections"
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {"cm_sx_bloods_taken": BloodTests.objects.filter(Q(name=NONE))}
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_cm_sx_bloods_taken_single_selection_only_for_na(self):
        cleaned_data = self.get_valid_patient_with_signs_or_symptoms()
        cleaned_data.update(
            {
                "cm_sx": NO,
                "cm_sx_bloods_taken": BloodTests.objects.filter(
                    Q(name=NOT_APPLICABLE) | Q(name="chemistry")
                ),
            }
        )
        self.assertFormValidatorError(
            field="cm_sx_bloods_taken",
            expected_msg=(
                "Invalid combination. "
                "'--Not applicable (if no signs or symptoms related to CM)' "
                "may not be combined with other selections"
            ),
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update(
            {"cm_sx_bloods_taken": BloodTests.objects.filter(Q(name=NOT_APPLICABLE))}
        )
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_cm_sx_bloods_taken_other_required_if_other_selected(self):
        cleaned_data = self.get_valid_patient_with_cm_symptoms()
        cleaned_data.update(
            {
                "cm_sx_bloods_taken": BloodTests.objects.filter(name=OTHER),
                "cm_sx_bloods_taken_other": "",
            }
        )
        self.assertFormValidatorError(
            field="cm_sx_bloods_taken_other",
            expected_msg="This field is required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"cm_sx_bloods_taken_other": "Some other blood test"})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_cm_sx_bloods_taken_other_not_required_if_other_not_selected(self):
        cleaned_data = self.get_valid_patient_with_cm_symptoms()
        cleaned_data.update(
            {
                "cm_sx_bloods_taken": BloodTests.objects.filter(name="chemistry"),
                "cm_sx_bloods_taken_other": "Some other blood test",
            }
        )
        self.assertFormValidatorError(
            field="cm_sx_bloods_taken_other",
            expected_msg="This field is not required.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        cleaned_data.update({"cm_sx_bloods_taken_other": ""})
        self.assertFormValidatorNoError(
            form_validator=self.validate_form_validator(cleaned_data)
        )

    def test_cm_sx_patient_admitted_applicable_if_cm_sx_yes(self):
        cleaned_data = self.get_valid_patient_with_cm_symptoms()
        cleaned_data.update(
            {
                "cm_sx": YES,
                "cm_sx_patient_admitted": NOT_APPLICABLE,
            }
        )
        self.assertFormValidatorError(
            field="cm_sx_patient_admitted",
            expected_msg="This field is applicable.",
            form_validator=self.validate_form_validator(cleaned_data),
        )

        for answer in [YES, NO]:
            with self.subTest(answer=answer):
                cleaned_data.update({"cm_sx_patient_admitted": answer})
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_cm_sx_patient_admitted_not_applicable_if_cm_sx_not_yes(self):
        for cm_sx_answer in [NO, NOT_APPLICABLE]:
            for cm_sx_patient_admitted_answer in [YES, NO]:
                with self.subTest(
                    cm_sx_answer=cm_sx_answer,
                    cm_sx_patient_admitted_answer=cm_sx_patient_admitted_answer,
                ):
                    cleaned_data = (
                        self.get_valid_patient_with_signs_or_symptoms()
                        if cm_sx_answer == NO
                        else self.get_valid_patient_any_sx_unknown()
                    )
                    cleaned_data.update(
                        {
                            "cm_sx": cm_sx_answer,
                            "cm_sx_patient_admitted": cm_sx_patient_admitted_answer,
                        }
                    )
                    self.assertFormValidatorError(
                        field="cm_sx_patient_admitted",
                        expected_msg="This field is not applicable",
                        form_validator=self.validate_form_validator(cleaned_data),
                    )

                    cleaned_data.update({"cm_sx_patient_admitted": NOT_APPLICABLE})
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data)
                    )
