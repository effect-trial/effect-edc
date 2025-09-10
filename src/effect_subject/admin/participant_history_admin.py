from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import ParticipantHistoryForm
from ..models import ParticipantHistory
from .modeladmin import CrfModelAdmin


@admin.register(ParticipantHistory, site=effect_subject_admin)
class ParticipantHistoryAdmin(CrfModelAdmin):
    form = ParticipantHistoryForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        ("Inpatient status", {"fields": ("inpatient", "admission_indication")}),
        (
            "Fluconazole",
            {
                "description": "Only complete at Day 1",
                "fields": (
                    "flucon_1w_prior_rando",
                    "flucon_days",
                    "flucon_dose",
                    "flucon_dose_other",
                    "flucon_dose_other_reason",
                ),
            },
        ),
        (
            "Neurological",
            {"fields": ("reported_neuro_abnormality", "neuro_abnormality_details")},
        ),
        (
            "TB diagnosis",
            {
                "fields": (
                    "tb_prev_dx",
                    "tb_dx_date",
                    "tb_dx_date_estimated",
                    "tb_site",
                )
            },
        ),
        (
            "TB prevention/treatment",
            {
                "fields": (
                    "on_tb_tx",
                    "tb_tx_type",
                    "active_tb_tx",
                )
            },
        ),
        (
            "Other opportunistic infections",
            {"fields": ("previous_oi", "previous_oi_name", "previous_oi_dx_date")},
        ),
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

    filter_horizontal = ["active_tb_tx", "specify_medications"]

    radio_fields = {
        "any_medications": admin.VERTICAL,
        "flucon_1w_prior_rando": admin.VERTICAL,
        "flucon_dose": admin.VERTICAL,
        "inpatient": admin.VERTICAL,
        "on_tb_tx": admin.VERTICAL,
        "previous_oi": admin.VERTICAL,
        "reported_neuro_abnormality": admin.VERTICAL,
        "tb_dx_date_estimated": admin.VERTICAL,
        "tb_prev_dx": admin.VERTICAL,
        "tb_site": admin.VERTICAL,
        "tb_tx_type": admin.VERTICAL,
    }
