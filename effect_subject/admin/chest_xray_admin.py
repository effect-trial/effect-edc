from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import ChestXrayForm
from ..models import ChestXray
from .modeladmin import CrfModelAdmin


@admin.register(ChestXray, site=effect_subject_admin)
class ChestXrayAdmin(CrfModelAdmin):
    form = ChestXrayForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Chest x-ray",
            {
                "fields": (
                    "chest_xray",
                    "chest_xray_date",
                    "chest_xray_results",
                    "chest_xray_results_other",
                    "comment",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = ["chest_xray_results"]

    radio_fields = {
        "chest_xray": admin.VERTICAL,
    }
