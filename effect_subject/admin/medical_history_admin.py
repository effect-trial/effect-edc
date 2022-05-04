from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import MedicalHistoryForm
from ..models import MedicalHistory
from .modeladmin import CrfModelAdmin


@admin.register(MedicalHistory, site=effect_subject_admin)
class MedicalHistoryAdmin(CrfModelAdmin):

    form = MedicalHistoryForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "TB diagnosis/treatment",
            {
                "fields": (
                    "tb_prev_dx",
                    "tb_site",
                    "on_tb_tx",
                    "tb_dx_ago",
                    "on_rifampicin",
                    "rifampicin_start_date",
                )
            },
        ),
        (
            "Other opportunistic infections",
            {"fields": ("previous_oi", "previous_oi_name", "previous_oi_dx_date")},
        ),
        ("HIV diagnosis", {"fields": ("new_hiv_dx", "hiv_dx_date")}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "new_hiv_dx": admin.VERTICAL,
        "previous_oi": admin.VERTICAL,
        "on_rifampicin": admin.VERTICAL,
        "tb_dx_ago": admin.VERTICAL,
        "tb_prev_dx": admin.VERTICAL,
        "tb_site": admin.VERTICAL,
        "on_tb_tx": admin.VERTICAL,
    }
