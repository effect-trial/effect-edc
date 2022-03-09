from django import forms
from django.utils.translation import gettext_lazy as _
from edc_adverse_event.forms import AeInitialModelFormMixin

from ..models import AeInitial


class AeInitialForm(AeInitialModelFormMixin, forms.ModelForm):
    class Meta:
        model = AeInitial
        fields = "__all__"
        labels = {
            "ae_cause": _(
                "Has a reason other than the study drugs been "
                "identified as the cause of the event(s)?"
            ),
        }
        help_texts = {
            "ae_description": _(
                "Record Diagnosis if available. "
                "Include anatomical location, if applicable. "
                "Please note concurrent ARVs/other medications etc."
            ),
        }
