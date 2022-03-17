from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import effect_subject_admin
from ...forms import AdherenceForm
from ...models import Adherence
from ..modeladmin import CrfModelAdmin


@admin.register(Adherence, site=effect_subject_admin)
class AdherenceAdmin(CrfModelAdmin):

    form = AdherenceForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Adherence counselling",
            {
                "fields": (
                    "adherence_counselling",
                    "adherence_counselling_reason_no",
                    "diary_issued",
                    "diary_issued_reason_no",
                )
            },
        ),
        (
            "Missed doses",
            {
                "fields": (
                    "any_doses_missed",
                    "fluconazole_doses_missed",
                    "flucytosine_doses_missed",
                )
            },
        ),
        (
            "Pill count and adherence diary review",
            {
                "fields": (
                    "pill_count_conducted",
                    "pill_count_conducted_reason_no",
                    "diary_returned",
                    "diary_returned_reason_no",
                    "diary_match_pill_count",
                    "diary_match_pill_count_reason_no",
                )
            },
        ),
        (
            "Adherence summary",
            {
                "fields": (
                    "opinion_fluconazole_adherent",
                    "opinion_art_adherent",
                    "adherence_narrative",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "adherence_counselling": admin.VERTICAL,
        "any_doses_missed": admin.VERTICAL,
        "diary_issued": admin.VERTICAL,
        "diary_match_pill_count": admin.VERTICAL,
        "diary_returned": admin.VERTICAL,
        "opinion_art_adherent": admin.VERTICAL,
        "opinion_fluconazole_adherent": admin.VERTICAL,
        "pill_count_conducted": admin.VERTICAL,
    }
