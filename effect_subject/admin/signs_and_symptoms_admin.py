from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import (
    ModelAdminActionItemMixin,
    action_fields,
    action_fieldset_tuple,
)
from edc_model_admin import SimpleHistoryAdmin

from effect_subject.admin.fieldsets import reporting_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import SignsAndSymptomsForm
from ..models import SignsAndSymptoms
from .modeladmin import CrfModelAdminMixin


@admin.register(SignsAndSymptoms, site=effect_subject_admin)
class SignsAndSymptomsAdmin(
    CrfModelAdminMixin,
    ModelAdminActionItemMixin,
    SimpleHistoryAdmin,
):

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
                    "cm_sx",
                    "current_sx_gte_g3",
                    "current_sx_gte_g3_other",
                )
            },
        ),
        (
            "Additional details",
            {
                "fields": (
                    "headache_duration",
                    # "headache_duration_microseconds",
                    "cn_palsy_left_other",
                    "cn_palsy_right_other",
                    "focal_neurologic_deficit_other",
                    "visual_field_loss",
                )
            },
        ),
        (
            "Investigations",
            {
                "fields": (
                    "xray_performed",
                    "lp_performed",
                    "urinary_lam_performed",
                )
            },
        ),
        reporting_fieldset_tuple,
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = [
        "current_sx",
        "current_sx_gte_g3",
    ]

    readonly_fields = action_fields

    radio_fields = {
        "any_sx": admin.VERTICAL,
        "cm_sx": admin.VERTICAL,
        "lp_performed": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
        "reportable_as_ae": admin.VERTICAL,
        "urinary_lam_performed": admin.VERTICAL,
        "xray_performed": admin.VERTICAL,
    }
