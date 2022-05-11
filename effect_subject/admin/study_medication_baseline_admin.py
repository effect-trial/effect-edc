from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django_audit_fields.admin import audit_fieldset_tuple
from edc_visit_tracking.utils import get_subject_visit_model_cls

from ..admin_site import effect_subject_admin
from ..forms import StudyMedicationBaselineForm
from ..models import StudyMedicationBaseline
from .modeladmin import CrfModelAdmin


@admin.register(StudyMedicationBaseline, site=effect_subject_admin)
class StudyMedicationBaselineAdmin(CrfModelAdmin):

    form = StudyMedicationBaselineForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Fluconazole",
            {
                "fields": (
                    "flucon_initiated",
                    "flucon_not_initiated_reason",
                    "flucon_dose",
                    "flucon_dose_datetime",
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
                    "flucyt_dose",
                    "flucyt_dose_datetime",
                    "flucyt_notes",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "flucyt_initiated": admin.VERTICAL,
        "flucon_initiated": admin.VERTICAL,
    }

    def get_changeform_initial_data(self, request):
        initial_data = super().get_changeform_initial_data(request)
        try:
            subject_visit = get_subject_visit_model_cls().objects.get(
                id=request.GET.get(self.model.visit_model_attr())
            )
        except ObjectDoesNotExist:
            pass
        else:
            initial_data.update(
                report_datetime=subject_visit.report_datetime,
            )
        return initial_data
