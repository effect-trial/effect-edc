from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_microbiology.modeladmin_mixins import BloodCultureModelAdminMixin

from ..admin_site import effect_subject_admin
from ..forms import BloodCultureForm
from ..models import BloodCulture
from .modeladmin import CrfModelAdmin


def get_blood_culture_fieldset():
    return [
        "Blood Culture",
        {
            "fields": (
                "blood_culture_performed",
                "blood_culture_date",
                "blood_culture_result",
                "blood_culture_organism_text",
            )
        },
    ]


@admin.register(BloodCulture, site=effect_subject_admin)
class BloodCultureAdmin(BloodCultureModelAdminMixin, CrfModelAdmin):

    form = BloodCultureForm

    autocomplete_fields = ["requisition"]

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        get_blood_culture_fieldset(),
        ("Comment", {"fields": ("comment",)}),
        audit_fieldset_tuple,
    )
