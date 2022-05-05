from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_csf.fieldsets import (
    get_csf_culture_fieldset,
    get_csf_fieldset,
    get_lp_fieldset,
)
from edc_csf.modeladmin_mixins import LpCsfModelAdminMixin

from ..admin_site import effect_subject_admin
from ..forms import LpCsfForm
from ..models import LpCsf
from .modeladmin import CrfModelAdmin


@admin.register(LpCsf, site=effect_subject_admin)
class LpCsfAdmin(LpCsfModelAdminMixin, CrfModelAdmin):

    form = LpCsfForm

    autocomplete_fields = ["csf_requisition"]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        get_lp_fieldset(),
        get_csf_fieldset(),
        (
            get_csf_culture_fieldset(requisition_field="csf_requisition")[0],
            {
                "fields": tuple(
                    f
                    for f in get_csf_culture_fieldset(requisition_field="csf_requisition")[1][
                        "fields"
                    ]
                    if f not in {"csf_crag_immy_lfa"}
                )
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = ("lp_datetime", "reason_for_lp")

    list_filter = ("lp_datetime", "reason_for_lp")

    radio_fields = {
        "reason_for_lp": admin.VERTICAL,
        "opening_pressure_measured": admin.VERTICAL,
        "csf_culture": admin.VERTICAL,
        "csf_crag": admin.VERTICAL,
        "csf_crag_lfa": admin.VERTICAL,
        "differential_lymphocyte_unit": admin.VERTICAL,
        "differential_neutrophil_unit": admin.VERTICAL,
        "csf_glucose_units": admin.VERTICAL,
        "csf_positive": admin.VERTICAL,
        "india_ink": admin.VERTICAL,
        "sq_crag": admin.VERTICAL,
        "sq_crag_pos": admin.VERTICAL,
        "crf_crag_titre_done": admin.VERTICAL,
    }
