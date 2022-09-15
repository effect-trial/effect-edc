from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import StudyMedicationFollowupForm
from ..models import StudyMedicationFollowup
from .modeladmin import CrfModelAdmin


@admin.register(StudyMedicationFollowup, site=effect_subject_admin)
class StudyMedicationFollowupAdmin(CrfModelAdmin):

    form = StudyMedicationFollowupForm

    fieldsets = (
        (
            None,
            {"fields": ("subject_visit", "report_datetime")},
        ),
        (
            "Modifications",
            {
                "fields": (
                    "modifications",
                    "modifications_reason",
                    "modifications_reason_other",
                )
            },
        ),
        (
            "Fluconazole",
            {
                "fields": (
                    "flucon_modified",
                    "flucon_dose_datetime",
                    "flucon_dose",
                    "flucon_notes",
                ),
            },
        ),
        (
            "Flucytosine",
            {
                "fields": (
                    "flucyt_modified",
                    "flucyt_dose_datetime",
                    "flucyt_dose",
                    "flucyt_dose_0400",
                    "flucyt_dose_1000",
                    "flucyt_dose_1600",
                    "flucyt_dose_2200",
                    "flucyt_notes",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "modifications": admin.VERTICAL,
        "flucon_modified": admin.VERTICAL,
        "flucyt_modified": admin.VERTICAL,
    }

    filter_horizontal = ("modifications_reason",)
