from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import ArvTreatmentForm
from ..models import ArvTreatment
from .modeladmin import CrfModelAdmin


@admin.register(ArvTreatment, site=effect_subject_admin)
class ArvTreatmentAdmin(CrfModelAdmin):
    form = ArvTreatmentForm

    autocomplete_fields = ("arv_regimen",)

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "ARV Treatment",
            {
                "fields": (
                    "on_arv_regimen",
                    "adherent",
                    "arv_regimen_stopped",
                    "arv_regimen_stopped_date",
                    "arv_regimen_changed",
                    "arv_regimen",
                    "arv_regimen_start_date",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "on_arv_regimen": admin.VERTICAL,
        "adherent": admin.VERTICAL,
        "arv_regimen_stopped": admin.VERTICAL,
        "arv_regimen_changed": admin.VERTICAL,
    }
