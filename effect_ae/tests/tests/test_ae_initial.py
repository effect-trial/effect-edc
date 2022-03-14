from django.test import TestCase, tag
from edc_adverse_event.choices import STUDY_DRUG_RELATIONSHIP
from edc_constants.constants import NO, NOT_APPLICABLE, UNKNOWN, YES

from effect_ae.constants import DEFINITELY_RELATED, NOT_RELATED
from effect_ae.form_validators import AeInitialFormValidator
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_subject.forms.followup_form import get_choice_display_text


@tag("aei")
class TestAeInitialFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = AeInitialFormValidator

    study_drugs = ["fluconazole", "flucytosine"]
    study_drug_relationships_choices = [choice[0] for choice in STUDY_DRUG_RELATIONSHIP]

    def test_study_relation_yes_valid_with_all_study_drug_choices(self):
        for study_drug in self.study_drugs:
            for choice in self.study_drug_relationships_choices:
                with self.subTest(study_drug=study_drug, choice=choice):
                    cleaned_data = {
                        "ae_study_relation_possibility": YES,
                        f"{study_drug}_relation": choice,
                    }
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data)
                    )

    def test_study_relation_no_valid_with_study_drug_not_related(self):
        for study_drug in self.study_drugs:
            with self.subTest(study_drug=study_drug):
                cleaned_data = {
                    "ae_study_relation_possibility": NO,
                    f"{study_drug}_relation": NOT_RELATED,
                }
                self.assertFormValidatorNoError(
                    form_validator=self.validate_form_validator(cleaned_data)
                )

    def test_study_relation_no_invalid_with_study_drug_relation_not_ruled_out(self):
        choices_subset = [
            choice
            for choice in self.study_drug_relationships_choices
            if choice != NOT_RELATED and choice != NOT_APPLICABLE
        ]
        for study_drug in self.study_drugs:
            for choice in choices_subset:
                with self.subTest(study_drug=study_drug, choice=choice):
                    cleaned_data = {
                        f"{study_drug}_relation": choice,
                        "ae_study_relation_possibility": NO,
                    }
                    self.assertFormValidatorError(
                        field="ae_study_relation_possibility",
                        expected_msg="Invalid. Cannot be 'No' if "
                        f"'{get_choice_display_text(STUDY_DRUG_RELATIONSHIP, choice)}' "
                        f"to study drug: {study_drug.title()}",
                        form_validator=self.validate_form_validator(cleaned_data),
                    )

    def test_study_relation_unknown_invalid_with_definite_study_drug_relation_choice(
        self,
    ):
        for study_drug in self.study_drugs:
            with self.subTest(study_drug=study_drug):
                cleaned_data = {
                    f"{study_drug}_relation": DEFINITELY_RELATED,
                    "ae_study_relation_possibility": UNKNOWN,
                }
                self.assertFormValidatorError(
                    field="ae_study_relation_possibility",
                    expected_msg="Invalid. Cannot be 'Unknown' if 'Definitely related' "
                    f"to study drug: {study_drug.title()}",
                    form_validator=self.validate_form_validator(cleaned_data),
                )

    def test_study_relation_unknown_valid_with_non_definite_study_drug_relation_choices(
        self,
    ):
        choices_subset = [
            value
            for value in self.study_drug_relationships_choices
            if value != DEFINITELY_RELATED
        ]
        for study_drug in self.study_drugs:
            for choice in choices_subset:
                with self.subTest(study_drug=study_drug, choice=choice):
                    cleaned_data = {
                        f"{study_drug}_relation": choice,
                        "ae_study_relation_possibility": UNKNOWN,
                    }
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data),
                    )
