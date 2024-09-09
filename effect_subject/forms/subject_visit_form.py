from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from edc_action_item.models import ActionItem
from edc_consent.modelform_mixins import RequiresConsentModelFormMixin
from edc_constants.constants import DEAD
from edc_form_validators import FormValidatorMixin
from edc_offstudy.modelform_mixins import OffstudyNonCrfModelFormMixin
from edc_utils import formatted_date
from edc_visit_tracking.modelform_mixins import VisitTrackingModelFormMixin
from effect_form_validators.effect_subject import SubjectVisitFormValidator

from effect_ae.action_items import DeathReportAction

from ..models import SubjectVisit


class SubjectVisitForm(
    RequiresConsentModelFormMixin,
    VisitTrackingModelFormMixin,
    OffstudyNonCrfModelFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):
    form_validator_cls = SubjectVisitFormValidator

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("survival_status") == DEAD:
            DeathReportAction(
                subject_identifier=cleaned_data.get("appointment").subject_identifier
            )
        else:
            try:
                obj = DeathReportAction.reference_model_cls().objects.get(
                    subject_identifier=cleaned_data.get("appointment").subject_identifier,
                )
            except ObjectDoesNotExist:
                ActionItem.objects.filter(
                    subject_identifier=cleaned_data.get("appointment").subject_identifier,
                    action_type__name=DeathReportAction.name,
                ).delete()
            else:
                if obj.death_datetime.date() <= self.report_datetime.date():
                    dt = formatted_date(obj.death_datetime.date())
                    raise forms.ValidationError(
                        {
                            "survival_status": (
                                "Invalid. A Death report has "
                                f"already been submitted for this participant. Got {dt}."
                            )
                        }
                    )
        return cleaned_data

    class Meta:
        model = SubjectVisit
        fields = "__all__"
        help_texts = {
            "survival_status": _("If subject deceased, complete Death report"),
        }
