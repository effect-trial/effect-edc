from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.modelform_mixins import SiteModelFormMixin
from effect_form_validators.effect_consent import SubjectConsentUpdateV2FormValidator

from ..models import SubjectConsentUpdateV2


class SubjectConsentUpdateV2Form(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = SubjectConsentUpdateV2FormValidator

    subject_identifier = forms.CharField(
        label="Subject identifier",
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    action_identifier = forms.CharField(
        label="Action identifier",
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = SubjectConsentUpdateV2
        fields = "__all__"
