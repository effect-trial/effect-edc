from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import PatientHistoryForm
from ..models import PatientHistory
from .modeladmin import CrfModelAdmin


@admin.register(PatientHistory, site=effect_subject_admin)
class PatientHistoryAdmin(CrfModelAdmin):

    form = PatientHistoryForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Previous treatment",
            {
                "description": "Only complete at Day 1",
                "fields": (
                    "fluconazole_1w_prior_rando",
                    "fluconazole_days",
                    "fluconazole_dose",
                    "fluconazole_dose_other",
                    "fluconazole_dose_other_reason",
                ),
            },
        ),
        ("ARV", {"fields": ("current_arv_decision",)}),
        (
            "Neurological",
            {"fields": ("reported_neuro_abnormality", "neuro_abnormality_details")},
        ),
        ("Lung exam", {"fields": ("abnormal_lung_exam",)}),
        (
            "Other medication",
            {
                "fields": (
                    "any_medications",
                    "specify_medications",
                    "specify_steroid_other",
                    "specify_medications_other",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = ["specify_medications"]

    radio_fields = {
        "abnormal_lung_exam": admin.VERTICAL,
        "any_medications": admin.VERTICAL,
        "current_arv_decision": admin.VERTICAL,
        "fluconazole_1w_prior_rando": admin.VERTICAL,
        "fluconazole_dose": admin.VERTICAL,
        "reported_neuro_abnormality": admin.VERTICAL,
    }
