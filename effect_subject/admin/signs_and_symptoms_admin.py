from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import SignsAndSymptomsForm
from ..models import SignsAndSymptoms
from .modeladmin import CrfModelAdmin


@admin.register(SignsAndSymptoms, site=effect_subject_admin)
class SignsAndSymptomsAdmin(CrfModelAdmin):

    form = SignsAndSymptomsForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Signs and symptoms",
            {
                "fields": (
                    "any_sx",
                    "current_sx",
                    "current_sx_other",
                    "reportable_as_ae",
                    "current_sx_gte_g3",
                    "current_sx_gte_g3_other",
                    "headache_duration",
                    # "headache_duration_microseconds",
                    "visual_field_loss",
                )
            },
        ),
        (
            "Reporting",
            {"fields": ("patient_admitted",)},
        ),
        (
            "CM signs and symptoms",
            {
                "fields": (
                    "cm_sx",
                    "cm_sx_lp_done",
                    "cm_sx_bloods_taken",
                    "cm_sx_patient_admitted",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = [
        "current_sx",
        "current_sx_gte_g3",
    ]

    radio_fields = {
        "any_sx": admin.VERTICAL,
        "cm_sx": admin.VERTICAL,
        "cm_sx_bloods_taken": admin.VERTICAL,
        "cm_sx_lp_done": admin.VERTICAL,
        "cm_sx_patient_admitted": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
        "reportable_as_ae": admin.VERTICAL,
    }
