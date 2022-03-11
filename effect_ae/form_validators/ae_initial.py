from django import forms
from edc_adverse_event.form_validators import AeInitialFormValidator as FormValidator
from edc_constants.constants import UNKNOWN

from effect_ae.constants import DEFINITELY_RELATED


class AeInitialFormValidator(FormValidator):
    def clean(self):
        super().clean()
        # TODO: Validate hospitalization section

        self.validate_study_relation_possibility()

    def validate_study_relation_possibility(self):
        for study_drug in ["fluconazole", "flucytosine"]:
            if (
                self.cleaned_data.get(f"{study_drug}_relation") == DEFINITELY_RELATED
                and self.cleaned_data.get("ae_study_relation_possibility") == UNKNOWN
            ):
                raise forms.ValidationError(
                    {
                        "ae_study_relation_possibility": (
                            "Invalid. Cannot be 'Unknown' if 'Definitely related' "
                            f"to study drug: {study_drug.title()}"
                        )
                    }
                )

        # TODO validate: "ae_study_relation_possibility" N if drug unk/poss/prob/def related

    def validate_relationship_to_study_drug(self):
        # TODO: Flucytosine only applicable if a study drug (i.e. on that arm of trial)
        pass
