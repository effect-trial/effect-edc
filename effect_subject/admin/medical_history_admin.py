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
                    "tb_history",
                    "tb_site",
                    "tb_tx",
                    "tb_dx_ago",
                    "taking_rifampicin",
                    "rifampicin_started_date",
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
        "taking_rifampicin": admin.VERTICAL,
        "tb_dx_ago": admin.VERTICAL,
        "tb_history": admin.VERTICAL,
        "tb_site": admin.VERTICAL,
        "tb_tx": admin.VERTICAL,
    }
