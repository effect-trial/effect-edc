from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import PatientTreatmentDay14Form
from ..models import PatientTreatmentDay14
from .modeladmin import CrfModelAdmin


@admin.register(PatientTreatmentDay14, site=effect_subject_admin)
class PatientTreatmentDay14Admin(CrfModelAdmin):

    form = PatientTreatmentDay14Form

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Patient treatment at Day 14",
            {
                "fields": (
                    "other_antibiotics_first_2w",
                    "other_antibiotics_first_2w_other",
                    "other_drugs_first_2w",
                    "other_drugs_first_2w_other",
                    "fluconazole_rx_d14",
                    "fluconazole_rx_d14_other",
                    "fluconazole_rx_d14_other_reason",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = [
        "other_antibiotics_first_2w",
        "other_drugs_first_2w",
    ]

    radio_fields = {"fluconazole_rx_d14": admin.VERTICAL}
