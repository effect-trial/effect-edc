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
        ("HIV Diagnosis", {"fields": ("hiv_dx_date", "hiv_dx_date_estimated")}),
        (
            "ARV treatment and monitoring",
            {
                "fields": (
                    "on_art_at_crag",
                    "ever_on_art",
                    "initial_art_date",
                    "initial_art_date_estimated",
                    "initial_art_regimen",
                    "initial_art_regimen_other",
                    "has_switched_art_regimen",
                    "current_art_date",
                    "current_art_date_estimated",
                    "current_art_regimen",
                    "current_art_regimen_other",
                ),
            },
        ),
        (
            "ART adherence",
            {
                "fields": (
                    "has_defaulted",
                    "defaulted_date",
                    "defaulted_date_estimated",
                    "is_adherent",
                    "art_doses_missed",
                ),
            },
        ),
        (
            "ART decision",
            {
                "fields": ("art_decision",),
            },
        ),
        (
            "Viral load",
            {
                "fields": (
                    "has_viral_load_result",
                    "viral_load_result",
                    "viral_load_quantifier",
                    "viral_load_date",
                    "viral_load_date_estimated",
                ),
            },
        ),
        (
            "CD4 count",
            {
                "fields": (
                    "cd4_value",
                    "cd4_date",
                    "cd4_date_estimated",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = (
        "initial_art_regimen",
        "current_art_regimen",
    )

    radio_fields = {  # noqa: RUF012
        "art_decision": admin.VERTICAL,
        "cd4_date_estimated": admin.VERTICAL,
        "current_art_date_estimated": admin.VERTICAL,
        "defaulted_date_estimated": admin.VERTICAL,
        "ever_on_art": admin.VERTICAL,
        "has_defaulted": admin.VERTICAL,
        "has_switched_art_regimen": admin.VERTICAL,
        "has_viral_load_result": admin.VERTICAL,
        "hiv_dx_date_estimated": admin.VERTICAL,
        "initial_art_date_estimated": admin.VERTICAL,
        "is_adherent": admin.VERTICAL,
        "on_art_at_crag": admin.VERTICAL,
        "viral_load_date_estimated": admin.VERTICAL,
        "viral_load_quantifier": admin.VERTICAL,
    }
