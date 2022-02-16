from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_microbiology.fieldsets import (
    get_blood_culture_fieldset,
    get_csf_fieldset,
    get_histopathology_fieldset,
    get_sputum_fieldset,
    get_urine_culture_fieldset,
)
from edc_microbiology.modeladmin_mixin import MicrobiologyModelAdminMixin

from ..admin_site import effect_subject_admin
from ..forms import MicrobiologyForm
from ..models import Microbiology
from .modeladmin import CrfModelAdmin


@admin.register(Microbiology, site=effect_subject_admin)
class MicrobiologyAdmin(MicrobiologyModelAdminMixin, CrfModelAdmin):

    form = MicrobiologyForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        get_urine_culture_fieldset(),
        get_blood_culture_fieldset(),
        get_sputum_fieldset(),
        get_csf_fieldset(),
        get_histopathology_fieldset(),
        audit_fieldset_tuple,
    )
