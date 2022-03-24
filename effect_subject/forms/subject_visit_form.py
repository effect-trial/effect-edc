from django import forms
from django.utils.translation import gettext_lazy as _
from edc_constants.choices import ALIVE_DEAD_UNKNOWN
from edc_constants.constants import ALIVE, YES
from edc_constants.utils import get_display
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from edc_visit_schedule.constants import DAY1
from edc_visit_tracking.form_validators import VisitFormValidator

from ..constants import IN_PERSON, PATIENT, TELEPHONE
from ..models import SubjectVisit


class SubjectVisitFormValidator(VisitFormValidator):
    validate_missed_visit_reason = False

    @staticmethod
    def is_baseline_appointment(appointment) -> bool:
        return appointment.visit_code == DAY1 and appointment.visit_code_sequence == 0

    def clean(self):
        super().clean()
        if (
            self.is_baseline_appointment(self.cleaned_data.get("appointment"))
            and self.cleaned_data.get("assessment_type") == TELEPHONE
        ):
            raise forms.ValidationError(
                {"assessment_type": "Invalid. Expected 'In person' at baseline"}
            )

        self.validate_other_specify(field="assessment_type")

        self.validate_other_specify(field="assessment_who")

        self.validate_survival_status()

        if (
            self.is_baseline_appointment(self.cleaned_data.get("appointment"))
            and self.cleaned_data.get("hospitalized") == YES
        ):
            raise forms.ValidationError(
                {"hospitalized": "Invalid. Expected NO at baseline"}
            )

    def validate_survival_status(self):
        if self.cleaned_data.get("survival_status") != ALIVE:
            error_msg = None

            if self.is_baseline_appointment(self.cleaned_data.get("appointment")):
                survival_status = get_display(
                    ALIVE_DEAD_UNKNOWN, self.cleaned_data.get("survival_status")
                )
                error_msg = f"Invalid: Cannot be '{survival_status}' at baseline"

            elif self.cleaned_data.get("assessment_type") == IN_PERSON:
                error_msg = "Invalid: Expected 'Alive' if this is an 'In person' visit"

            elif self.cleaned_data.get("assessment_who") == PATIENT:
                error_msg = "Invalid: Expected 'Alive' if spoke to 'Patient'"

            if error_msg:
                raise forms.ValidationError({"survival_status": error_msg})


class SubjectVisitForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = SubjectVisitFormValidator

    class Meta:
        model = SubjectVisit
        fields = "__all__"
        help_texts = {
            "survival_status": _("If subject deceased, complete Death report"),
        }
