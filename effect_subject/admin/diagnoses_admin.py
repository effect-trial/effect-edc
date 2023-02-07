from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import DiagnosesForm
from ..models import Diagnoses
from .fieldsets import reporting_fieldset_tuple
from .modeladmin import CrfModelAdmin


@admin.register(Diagnoses, site=effect_subject_admin)
class DiagnosesAdmin(CrfModelAdmin):
    form = DiagnosesForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Gastrointestinal side effects",
            {
                "fields": (
                    "gi_side_effects",
                    "gi_side_effects_details",
                )
            },
        ),
        (
            "Diagnoses",
            {"fields": ("has_diagnoses", "diagnoses", "diagnoses_other")},
        ),
        reporting_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = ["diagnoses"]

    radio_fields = {
        "gi_side_effects": admin.VERTICAL,
        "has_diagnoses": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
        "reportable_as_ae": admin.VERTICAL,
    }
