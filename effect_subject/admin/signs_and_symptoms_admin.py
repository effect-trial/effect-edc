from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import SignsAndSymptomsForm
from ..models import SignsAndSymptoms
from .fieldsets import reporting_fieldset_tuple
from .modeladmin import CrfModelAdmin


@admin.register(SignsAndSymptoms, site=effect_subject_admin)
class SignsAndSymptomsAdmin(CrfModelAdmin):

    form = SignsAndSymptomsForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "CM signs and symptoms",
            {"fields": ("cm_signs_symptoms",)},
        ),
        (
            "Signs and symptoms",
            {
                "fields": (
                    "signs_and_symptoms",
                    "headache_duration",
                    "visual_field_loss",
                )
            },
        ),
        reporting_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = ["signs_and_symptoms"]

    radio_fields = {
        "cm_signs_symptoms": admin.VERTICAL,
        "reportable_as_ae": admin.VERTICAL,
        "patient_admitted": admin.VERTICAL,
    }
