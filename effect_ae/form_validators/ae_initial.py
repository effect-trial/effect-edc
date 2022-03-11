from edc_adverse_event.form_validators import AeInitialFormValidator as FormValidator
from edc_constants.constants import UNKNOWN, YES


class AeInitialFormValidator(FormValidator):
    def validate_relationship_to_study_drug(self):
        # TODO: Flucytosine only applicable if a study drug (i.e. on that arm of trial)
        pass
