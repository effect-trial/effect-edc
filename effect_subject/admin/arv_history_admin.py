from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import ArvHistoryForm
from ..models import ArvHistory
from .modeladmin import CrfModelAdmin


@admin.register(ArvHistory, site=effect_subject_admin)
class ArvHistoryAdmin(CrfModelAdmin):

    form = ArvHistoryForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "ARV treatment and monitoring",
            {
                "fields": (
                    "taking_arv_at_crag",
                    "ever_taken_arv",
                    "initial_arv_date",
                    "initial_arv_date_estimated",
                    "initial_arv_regimen",
                    "initial_arv_regimen_other",
                    "has_switched_regimen",
                    "current_arv_date",
                    "current_arv_date_estimated",
                    "current_arv_regimen",
                    "current_arv_regimen_other",
                ),
            },
        ),
        (
            "ART adherence",
            {
                "fields": (
                    "current_arv_is_defaulted",
                    "current_arv_defaulted_date",
                    "current_arv_defaulted_date_estimated",
                    "current_arv_is_adherent",
                    "current_arv_tablets_missed",
                ),
            },
        ),
        (
            "Viral load",
            {
                "fields": (
                    "last_viral_load",
                    "viral_load_date",
                    "vl_date_estimated",
                ),
            },
        ),
        (
            "CD4 count",
            {
                "fields": (
                    "last_cd4",
                    "cd4_date",
                    "cd4_date_estimated",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = [
        "initial_arv_regimen",
        "current_arv_regimen",
    ]

    radio_fields = {
        "cd4_date_estimated": admin.VERTICAL,
        "current_arv_date_estimated": admin.VERTICAL,
        "current_arv_defaulted_date_estimated": admin.VERTICAL,
        "current_arv_is_adherent": admin.VERTICAL,
        "current_arv_is_defaulted": admin.VERTICAL,
        "ever_taken_arv": admin.VERTICAL,
        "has_switched_regimen": admin.VERTICAL,
        "initial_arv_date_estimated": admin.VERTICAL,
        "taking_arv_at_crag": admin.VERTICAL,
        "vl_date_estimated": admin.VERTICAL,
    }
