from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import SignsAndSymptomsForm
from ..models import SignsAndSymptoms
from .modeladmin import CrfModelAdmin


@admin.register(SignsAndSymptoms, site=effect_subject_admin)
class SignsAndSymptomsAdmin(CrfModelAdmin):

    form = SignsAndSymptomsForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Signs and symptoms",
            {
                "fields": (
                    "any_signs_symptoms",
                    "signs_and_symptoms",
                    "reportable_as_ae",
                    "signs_and_symptoms_gte_g3",
                    "headache_duration",
                    # "headache_duration_microseconds",
                    "visual_field_loss",
                )
            },
        ),
        (
            "Reporting",
            {"fields": ("patient_admitted",)},
        ),
        (
            "CM signs and symptoms",
            {"fields": ("cm_signs_symptoms",)},
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = [
        "signs_and_symptoms",
        "signs_and_symptoms_gte_g3",
    ]

    radio_fields = {
        "any_signs_symptoms": admin.VERTICAL,
        "cm_signs_symptoms": admin.VERTICAL,
        "reportable_as_ae": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
    }
