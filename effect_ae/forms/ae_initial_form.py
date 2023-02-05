from django import forms
from django.utils.translation import gettext_lazy as _
from edc_adverse_event.modelform_mixins import AeInitialModelFormMixin

from ..form_validators import AeInitialFormValidator
from ..models import AeInitial


class AeInitialForm(AeInitialModelFormMixin, forms.ModelForm):
    form_validator_cls = AeInitialFormValidator

    class Meta(AeInitialModelFormMixin.Meta):
        model = AeInitial
        fields = "__all__"
        labels = {
            "ae_cause": _("Has any cause other than study medication been identified?"),
        }
        help_texts = AeInitialModelFormMixin.Meta.help_texts | {
            "ae_description": _(
                "Record Diagnosis if available. "
                "Include anatomical location, if applicable. "
                "Please note concurrent ARVs/other medications etc."
            ),
        }
