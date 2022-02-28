from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import HealthEconomicsForm
from ..models import HealthEconomics
from .modeladmin import CrfModelAdmin


@admin.register(HealthEconomics, site=effect_subject_admin)
class HealthEconomicsAdmin(CrfModelAdmin):

    form = HealthEconomicsForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        audit_fieldset_tuple,
    )
