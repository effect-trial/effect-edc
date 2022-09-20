from django import forms
from edc_crf.modelform_mixins import CrfModelFormMixin
from effect_form_validators.effect_subject import StudyMedicationFollowupFormValidator

from ..models import StudyMedicationFollowup


class StudyMedicationFollowupForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = StudyMedicationFollowupFormValidator

    class Meta:
        model = StudyMedicationFollowup
        fields = "__all__"
        labels = {
            "flucon_dose_datetime": "Date and time modified fluconazole dose administered",
            "flucon_next_dose": "Modified fluconazole dose administered",
            "flucyt_dose_datetime": "Date and time modified flucytosine dose administered",
            "flucyt_next_dose": "Modified flucytosine dose administered",
        }
