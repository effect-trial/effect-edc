from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_microbiology.modeladmin_mixins import HistopathologyModelAdminMixin

from ..admin_site import effect_subject_admin
from ..forms import HistopathologyForm
from ..models import Histopathology
from .modeladmin import CrfModelAdmin


def get_histopathology_fieldset():
    return [
        "Histopathology",
        {
            "fields": (
                "tissue_biopsy_performed",
                "tissue_biopsy_date",
                "tissue_biopsy_result",
                "tissue_biopsy_organism_text",
            ),
        },
    ]


@admin.register(Histopathology, site=effect_subject_admin)
class HistopathologyAdmin(HistopathologyModelAdminMixin, CrfModelAdmin):
    form = HistopathologyForm

    autocomplete_fields = ("requisition",)

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        get_histopathology_fieldset(),
        ("Comment", {"fields": ("comment",)}),
        audit_fieldset_tuple,
    )
