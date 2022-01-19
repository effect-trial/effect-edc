from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import VitalSignsForm
from ..models import VitalSigns
from .fieldsets import reporting_fieldset_tuple
from .modeladmin import CrfModelAdmin


@admin.register(VitalSigns, site=effect_subject_admin)
class VitalSignsAdmin(CrfModelAdmin):

    form = VitalSignsForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Vital signs",
            {
                "fields": (
                    "weight",
                    "weight_measured_or_est",
                    "heart_rate",
                    "respiratory_rate",
                    "temperature",
                )
            },
        ),
        reporting_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "weight_measured_or_est": admin.VERTICAL,
        "reportable_as_ae": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
    }
