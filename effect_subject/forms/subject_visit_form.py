from django import forms
from django.utils.translation import gettext_lazy as _
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from effect_form_validators.effect_subject import SubjectVisitFormValidator

from ..models import SubjectVisit


class SubjectVisitForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = SubjectVisitFormValidator

    class Meta:
        model = SubjectVisit
        fields = "__all__"
        help_texts = {
            "survival_status": _("If subject deceased, complete Death report"),
        }
