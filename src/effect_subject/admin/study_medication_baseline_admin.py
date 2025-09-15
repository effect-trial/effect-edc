from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from django_audit_fields.admin import audit_fieldset_tuple
from edc_visit_tracking.utils import get_related_visit_model_cls

from ..admin_site import effect_subject_admin
from ..forms import StudyMedicationBaselineForm
from ..models import StudyMedicationBaseline
from .modeladmin import CrfModelAdmin


@admin.register(StudyMedicationBaseline, site=effect_subject_admin)
class StudyMedicationBaselineAdmin(CrfModelAdmin):
    form = StudyMedicationBaselineForm

    additional_instructions = mark_safe(
        "Please ensure the baseline Vital Signs form has been completed for "
        "participant <strong>before</strong> starting this form.",
    )  # nosec #B703 # B308

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Fluconazole",
            {
                "fields": (
                    "flucon_initiated",
                    "flucon_not_initiated_reason",
                    "flucon_dose_datetime",
                    "flucon_dose",
                    "flucon_next_dose",
                    "flucon_notes",
                ),
            },
        ),
        (
            "Flucytosine",
            {
                "fields": (
                    "flucyt_initiated",
                    "flucyt_not_initiated_reason",
                    "flucyt_dose_datetime",
                    "flucyt_dose_expected",
                    "flucyt_dose",
                    "flucyt_dose_0400",
                    "flucyt_dose_1000",
                    "flucyt_dose_1600",
                    "flucyt_dose_2200",
                    "flucyt_next_dose",
                    "flucyt_notes",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "flucon_initiated": admin.VERTICAL,
        "flucon_next_dose": admin.VERTICAL,
        "flucyt_initiated": admin.VERTICAL,
        "flucyt_next_dose": admin.VERTICAL,
    }

    def get_changeform_initial_data(self, request):
        initial_data = super().get_changeform_initial_data(request)
        try:
            subject_visit = get_related_visit_model_cls().objects.get(
                id=request.GET.get(self.model.related_visit_model_attr()),
            )
        except ObjectDoesNotExist:
            pass
        else:
            initial_data.update(
                report_datetime=subject_visit.report_datetime,
            )
        return initial_data
