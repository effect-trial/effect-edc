from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import PatientTreatmentForm
from ..models import PatientTreatment
from .modeladmin import CrfModelAdmin


@admin.register(PatientTreatment, site=effect_subject_admin)
class PatientTreatmentAdmin(CrfModelAdmin):

    form = PatientTreatmentForm
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Cryptococcal meningitis",
            {
                "fields": (
                    "lp_completed",
                    "cm_confirmed",
                    "cm_tx",
                    "cm_tx_given",
                    "cm_tx_given_other",
                ),
            },
        ),
        (
            "Tuberculosis",
            {
                "fields": (
                    "tb_tx",
                    "tb_tx_date",
                    "tb_tx_given",
                    "tb_tx_given_other",
                    "tb_tx_reason_no",
                    "tb_tx_reason_no_other",
                )
            },
        ),
        (
            "Steroids",
            {
                "fields": (
                    "steroids",
                    "steroids_date",
                    "steroids_given",
                    "steroids_given_other",
                    "steroids_course",
                )
            },
        ),
        (
            "Co-trimixazole",
            {
                "fields": (
                    "co_trimoxazole",
                    "co_trimoxazole_date",
                    "co_trimoxazole_reason_no",
                    "co_trimoxazole_reason_no_other",
                )
            },
        ),
        (
            "Antibiotics",
            {
                "fields": (
                    "antibiotics",
                    "antibiotics_date",
                    "antibiotics_given",
                    "antibiotics_given_other",
                )
            },
        ),
        (
            "Other drugs",
            {
                "fields": (
                    "other_drugs",
                    "other_drugs_date",
                    "other_drugs_given",
                    "other_drugs_given_other",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = ["tb_tx_given", "antibiotics_given", "other_drugs_given"]

    radio_fields = {
        "antibiotics": admin.VERTICAL,
        "cm_confirmed": admin.VERTICAL,
        "cm_tx": admin.VERTICAL,
        "cm_tx_given": admin.VERTICAL,
        "co_trimoxazole": admin.VERTICAL,
        "co_trimoxazole_reason_no": admin.VERTICAL,
        "lp_completed": admin.VERTICAL,
        "other_drugs": admin.VERTICAL,
        "steroids": admin.VERTICAL,
        "steroids_given": admin.VERTICAL,
        "tb_tx": admin.VERTICAL,
        "tb_tx_reason_no": admin.VERTICAL,
    }
