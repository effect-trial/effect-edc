from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from edc_action_item.models import ActionItem
from edc_constants.constants import DEAD
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from effect_form_validators.effect_subject import SubjectVisitFormValidator

from effect_ae.action_items import DeathReportAction

from ..models import SubjectVisit


class SubjectVisitForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = SubjectVisitFormValidator

    def clean(self):
        if self.cleaned_data.get("survival_status") == DEAD:
            DeathReportAction(
                subject_identifier=self.cleaned_data.get("appointment").subject_identifier
            )
        else:
            try:
                DeathReportAction.reference_model_cls().objects.get(
                    subject_identifier=self.cleaned_data.get("appointment").subject_identifier
                )
            except ObjectDoesNotExist:
                ActionItem.objects.filter(
                    subject_identifier=self.cleaned_data.get("appointment").subject_identifier,
                    action_type__name=DeathReportAction.name,
                ).delete()
            else:
                raise forms.ValidationError(
                    {
                        "survival_status": (
                            "Invalid. A Death report has "
                            "already been submitted for this participant."
                        )
                    }
                )

    class Meta:
        model = SubjectVisit
        fields = "__all__"
        help_texts = {
            "survival_status": _("If subject deceased, complete Death report"),
        }
