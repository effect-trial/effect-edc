from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import MedicalHistoryForm
from ..models import MedicalHistory
from .modeladmin import CrfModelAdmin


@admin.register(MedicalHistory, site=effect_subject_admin)
class MedicalHistoryAdmin(CrfModelAdmin):

    form = MedicalHistoryForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        audit_fieldset_tuple,
    )

    radio_fields = {}
