from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import ParticipantTreatmentForm
from ..models import ParticipantTreatment
from .modeladmin import CrfModelAdmin


@admin.register(ParticipantTreatment, site=effect_subject_admin)
class ParticipantTreatmentAdmin(CrfModelAdmin):
    form = ParticipantTreatmentForm
    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Cryptococcal meningitis",
            {
                "fields": (
                    "lp_completed",
                    "cm_confirmed",
                    "on_cm_tx",
                    "cm_tx_given",
                    "cm_tx_given_other",
                ),
            },
        ),
        (
            "Tuberculosis",
            {
                "fields": (
                    "on_tb_tx",
                    "tb_tx_date",
                    "tb_tx_date_estimated",
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
                    "on_steroids",
                    "steroids_date",
                    "steroids_date_estimated",
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
                    "on_co_trimoxazole",
                    "co_trimoxazole_date",
                    "co_trimoxazole_date_estimated",
                    "co_trimoxazole_reason_no",
                    "co_trimoxazole_reason_no_other",
                )
            },
        ),
        (
            "Antibiotics",
            {
                "fields": (
                    "on_antibiotics",
                    "antibiotics_date",
                    "antibiotics_date_estimated",
                    "antibiotics_given",
                    "antibiotics_given_other",
                )
            },
        ),
        (
            "Other drugs",
            {
                "fields": (
                    "on_other_drugs",
                    "other_drugs_date",
                    "other_drugs_date_estimated",
                    "other_drugs_given",
                    "other_drugs_given_other",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = ["tb_tx_given", "antibiotics_given", "other_drugs_given"]

    radio_fields = {
        "antibiotics_date_estimated": admin.VERTICAL,
        "on_antibiotics": admin.VERTICAL,
        "cm_confirmed": admin.VERTICAL,
        "on_cm_tx": admin.VERTICAL,
        "cm_tx_given": admin.VERTICAL,
        "on_co_trimoxazole": admin.VERTICAL,
        "co_trimoxazole_date_estimated": admin.VERTICAL,
        "co_trimoxazole_reason_no": admin.VERTICAL,
        "lp_completed": admin.VERTICAL,
        "on_other_drugs": admin.VERTICAL,
        "other_drugs_date_estimated": admin.VERTICAL,
        "on_steroids": admin.VERTICAL,
        "steroids_date_estimated": admin.VERTICAL,
        "steroids_given": admin.VERTICAL,
        "on_tb_tx": admin.VERTICAL,
        "tb_tx_date_estimated": admin.VERTICAL,
        "tb_tx_reason_no": admin.VERTICAL,
    }
