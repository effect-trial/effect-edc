from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fields, action_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import VitalSignsForm
from ..models import VitalSigns
from .fieldsets import reporting_fieldset_tuple
from .modeladmin import CrfWithActionModelAdmin


@admin.register(VitalSigns, site=effect_subject_admin)
class VitalSignsAdmin(CrfWithActionModelAdmin):
    form = VitalSignsForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Vital signs",
            {
                "fields": (
                    "weight",
                    "weight_measured_or_est",
                    "sys_blood_pressure",
                    "dia_blood_pressure",
                    "heart_rate",
                    "respiratory_rate",
                    "temperature",
                    "abnormal_lung_exam",
                ),
            },
        ),
        action_fieldset_tuple,
        reporting_fieldset_tuple,
        audit_fieldset_tuple,
    )

    readonly_fields = action_fields

    radio_fields = {  # noqa: RUF012
        "abnormal_lung_exam": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
        "reportable_as_ae": admin.VERTICAL,
        "weight_measured_or_est": admin.VERTICAL,
    }
