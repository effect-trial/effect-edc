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
                    "current_sx_gte_g3",
                    "current_sx_gte_g3_other",
                    "headache_duration",
                    # "headache_duration_microseconds",
                    "cn_palsy_left_other",
                    "cn_palsy_right_other",
                    "focal_neurologic_deficit_other",
                    "visual_field_loss",
                )
            },
        ),
        reporting_fieldset_tuple,
        (
            "CM signs and symptoms",
            {
                "fields": (
                    "cm_sx",
                    "cm_sx_lp_done",
                    "cm_sx_bloods_taken",
                    "cm_sx_bloods_taken_other",
                    "cm_sx_patient_admitted",
                )
            },
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = [
        "current_sx",
        "current_sx_gte_g3",
        "cm_sx_bloods_taken",
    ]

    readonly_fields = action_fields

    radio_fields = {
        "any_sx": admin.VERTICAL,
        "cm_sx": admin.VERTICAL,
        "cm_sx_lp_done": admin.VERTICAL,
        "cm_sx_patient_admitted": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
        "reportable_as_ae": admin.VERTICAL,
    }
