from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import AdherenceForm
from ..models import Adherence
from .modeladmin import CrfModelAdmin


@admin.register(Adherence, site=effect_subject_admin)
class AdherenceAdmin(CrfModelAdmin):

    form = AdherenceForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        audit_fieldset_tuple,
    )
