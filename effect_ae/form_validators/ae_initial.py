from django import forms
from edc_adverse_event.choices import STUDY_DRUG_RELATIONSHIP
from edc_adverse_event.form_validators import AeInitialFormValidator as FormValidator
from edc_constants.choices import YES_NO_UNKNOWN
from edc_constants.constants import NO, UNKNOWN

from effect_ae.constants import (
    DEFINITELY_RELATED,
    POSSIBLY_RELATED,
    PROBABLY_RELATED,
    UNLIKELY_RELATED,
)
from effect_subject.forms.followup_form import get_choice_display_text


class AeInitialFormValidator(FormValidator):
    def clean(self):
        super().clean()
        # TODO: Validate hospitalization section

        self.validate_study_relation_possibility()

    def validate_study_relation_possibility(self):
        for study_drug in ["fluconazole", "flucytosine"]:
            if (
                self.cleaned_data.get("ae_study_relation_possibility") == NO
                and self.cleaned_data.get(f"{study_drug}_relation")
                in [
                    UNLIKELY_RELATED,
                    POSSIBLY_RELATED,
                    PROBABLY_RELATED,
                    DEFINITELY_RELATED,
                ]
            ) or (
                self.cleaned_data.get("ae_study_relation_possibility") == UNKNOWN
                and (
                    self.cleaned_data.get(f"{study_drug}_relation")
                    == DEFINITELY_RELATED
                )
            ):
                study_relation = get_choice_display_text(
                    YES_NO_UNKNOWN,
                    self.cleaned_data.get("ae_study_relation_possibility"),
                )
                drug_relation_choice = get_choice_display_text(
                    STUDY_DRUG_RELATIONSHIP,
                    self.cleaned_data.get(f"{study_drug}_relation"),
                )
                raise forms.ValidationError(
                    {
                        "ae_study_relation_possibility": (
                            f"Invalid. "
                            f"Cannot be '{study_relation}' if '{drug_relation_choice}' "
                            f"to study drug: {study_drug.title()}"
                        )
                    }
                )

    def validate_relationship_to_study_drug(self):
        # TODO: Flucytosine only applicable if a study drug (i.e. on that arm of trial)
        pass
