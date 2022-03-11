from django.test import TestCase, tag
from edc_adverse_event.choices import STUDY_DRUG_RELATIONSHIP
from edc_constants.constants import UNKNOWN

from effect_ae.constants import DEFINITELY_RELATED
from effect_ae.form_validators import AeInitialFormValidator
from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin


@tag("aei")
class TestAeInitialFormValidation(EffectTestCaseMixin, TestCase):

    form_validator_default_form_cls = AeInitialFormValidator

    def test_fluconazole_relation_definite_with_study_relation_unknown_invalid(self):
        cleaned_data = {
            "fluconazole_relation": DEFINITELY_RELATED,
            "ae_study_relation_possibility": UNKNOWN,
        }
        self.assertFormValidatorError(
            field="ae_study_relation_possibility",
            expected_msg="Invalid. Cannot be 'Unknown' if 'Definitely related' "
            "to study drug: Fluconazole",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_flucytosine_relation_definite_with_study_relation_unknown_invalid(self):
        cleaned_data = {
            "flucytosine_relation": DEFINITELY_RELATED,
            "ae_study_relation_possibility": UNKNOWN,
        }
        self.assertFormValidatorError(
            field="ae_study_relation_possibility",
            expected_msg="Invalid. Cannot be 'Unknown' if 'Definitely related' "
            "to study drug: Flucytosine",
            form_validator=self.validate_form_validator(cleaned_data),
        )

    def test_other_study_drug_relation_choices_with_study_relation_unknown_valid(self):
        relationship_choices = [
            choice[0]
            for choice in STUDY_DRUG_RELATIONSHIP
            if choice[0] != DEFINITELY_RELATED
        ]
        for study_drug in ["fluconazole", "flucytosine"]:
            for choice in relationship_choices:
                with self.subTest(study_drug=study_drug, choice=choice):
                    cleaned_data = {
                        f"{study_drug}_relation": choice,
                        "ae_study_relation_possibility": UNKNOWN,
                    }
                    self.assertFormValidatorNoError(
                        form_validator=self.validate_form_validator(cleaned_data),
                    )
