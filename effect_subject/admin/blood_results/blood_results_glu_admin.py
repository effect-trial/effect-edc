from django.contrib import admin
from edc_blood_results.admin import BloodResultsModelAdminMixin
from edc_blood_results.fieldsets import BloodResultFieldset
from edc_lab_panel.panels import blood_glucose_panel

from ...admin_site import effect_subject_admin
from ...forms import BloodResultsGluForm
from ...models import BloodResultsGlu
from ..modeladmin import CrfModelAdmin

# TODO: add is poc?


@admin.register(BloodResultsGlu, site=effect_subject_admin)
class BloodResultsGluAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsGluForm
    fieldsets = BloodResultFieldset(
        blood_glucose_panel,
        extra_fieldsets=((2, ("Fasting", {"fields": ["fasting"]})),),
    ).fieldsets

    radio_fields = {
        "fasting": admin.VERTICAL,
        "results_abnormal": admin.VERTICAL,
        "results_reportable": admin.VERTICAL,
    }
