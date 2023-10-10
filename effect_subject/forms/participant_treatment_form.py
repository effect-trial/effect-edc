from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators import INVALID_ERROR
from edc_visit_schedule.constants import DAY01
from edc_visit_tracking.utils import get_related_visit_model_cls
from effect_form_validators.effect_subject import ParticipantTreatmentFormValidator

from ..models import ParticipantTreatment


class ParticipantTreatmentForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = ParticipantTreatmentFormValidator

    def clean(self) -> dict:
        self.validate_on_tb_tx_against_baseline()
        return super().clean()

    @property
    def participant_history_model_cls(self):
        return django_apps.get_model("effect_subject.participanthistory")

    def validate_on_tb_tx_against_baseline(self):
        baseline_visit = get_related_visit_model_cls().objects.get(
            subject_identifier=self.related_visit.subject_identifier,
            visit_code=DAY01,
            visit_code_sequence=0,
        )
        try:
            participant_history = self.participant_history_model_cls.objects.get(
                subject_visit_id=baseline_visit.id
            )
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                {
                    "__all__": (
                        "Please complete the Day 1 "
                        f"{self.participant_history_model_cls._meta.verbose_name} "
                        f"form first."
                    )
                },
                INVALID_ERROR,
            )
        else:
            if (
                self.cleaned_data.get("on_tb_tx") == YES
                and participant_history.on_tb_tx == YES
            ):
                raise forms.ValidationError(
                    {
                        "on_tb_tx": (
                            "Invalid. "
                            "Participant indicated taking TB treatment in "
                            f"{self.participant_history_model_cls._meta.verbose_name} "
                            "form on Day 1 visit. Expected NO."
                        )
                    },
                    INVALID_ERROR,
                )

    class Meta:
        model = ParticipantTreatment
        fields = "__all__"
