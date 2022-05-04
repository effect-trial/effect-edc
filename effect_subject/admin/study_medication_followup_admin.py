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
        (None, {"fields": ("subject_visit", "report_datetime", "modifications")}),
        (
            "Fluconazole",
            {
                "fields": (
                    "flucon_dose",
                    "flucon_dose_datetime",
                    "flucon_notes",
                ),
            },
        ),
        (
            "Flucytosine",
            {
                "fields": (
                    "flucyt_dose",
                    "flucyt_dose_datetime",
                    "flucyt_notes",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "modifications": admin.VERTICAL,
    }
