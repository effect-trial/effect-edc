from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_microbiology.fieldsets import (
    get_sputum_afb_fieldset,
    get_sputum_culture_fieldset,
    get_sputum_genexpert_fieldset,
    get_urinary_lam_fieldset,
)
from edc_microbiology.modeladmin_mixins import MicrobiologyModelAdminMixin

from ..admin_site import effect_subject_admin
from ..forms import TbDiagnosticsForm
from ..models import TbDiagnostics
from .modeladmin import CrfModelAdmin


@admin.register(TbDiagnostics, site=effect_subject_admin)
class TbDiagnosticsAdmin(MicrobiologyModelAdminMixin, CrfModelAdmin):

    form = TbDiagnosticsForm

    autocomplete_fields = ["sputum_requisition"]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        get_urinary_lam_fieldset(),
        (
            "Sputum requisition",
            {
                "fields": ("sputum_requisition",),
                "description": (
                    "This requisition is required before proceeding to the next sections"
                ),
            },
        ),
        get_sputum_genexpert_fieldset(),
        get_sputum_culture_fieldset(),
        get_sputum_afb_fieldset(),
        ("Comment", {"fields": ("comment",)}),
        audit_fieldset_tuple,
    )

    search_fields = ("subject_visit__subject_identifier",)
