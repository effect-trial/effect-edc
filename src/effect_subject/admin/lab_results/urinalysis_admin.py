from django.contrib import admin
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset

from ...admin_site import effect_subject_admin
from ...forms import UrinalysisForm
from ...models import Urinalysis
from ..modeladmin import CrfModelAdmin


@admin.register(Urinalysis, site=effect_subject_admin)
class UrinalysisAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = UrinalysisForm
    fieldsets = BloodResultFieldset(Urinalysis.lab_panel, model_cls=Urinalysis).fieldsets
