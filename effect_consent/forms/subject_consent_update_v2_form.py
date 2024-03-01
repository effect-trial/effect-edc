from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.modelform_mixins import SiteModelFormMixin

from ..models import SubjectConsentUpdateV2


class SubjectConsentUpdateV2Form(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

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
