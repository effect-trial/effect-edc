from edc_adverse_event.form_validators import AeInitialFormValidator as FormValidator
from edc_constants.constants import UNKNOWN, YES


class AeInitialFormValidator(FormValidator):
    def validate_relationship_to_study_drug(self):
        drugs = [
            "fluconazole_relation",
            # TODO: Flucytosine only applicable if a study drug (i.e. on that arm of trial)
            "flucytosine_relation",
        ]
        for drug in drugs:
            self.applicable_if(
                YES,
                UNKNOWN,
                field="ae_study_relation_possibility",
                field_applicable=drug,
            )
