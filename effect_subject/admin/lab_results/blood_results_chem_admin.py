from django.contrib import admin
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset

from ...admin_site import effect_subject_admin
from ...forms import BloodResultsChemForm
from ...models import BloodResultsChem
from ..modeladmin import CrfModelAdmin


@admin.register(BloodResultsChem, site=effect_subject_admin)
class BloodResultsChemAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsChemForm
    fieldsets = BloodResultFieldset(
        BloodResultsChem.lab_panel, model_cls=BloodResultsChem
    ).fieldsets
