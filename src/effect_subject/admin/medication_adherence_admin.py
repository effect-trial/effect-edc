from django.contrib import admin
from edc_adherence.model_admin_mixin import MedicationAdherenceAdminMixin

from ..admin_site import effect_subject_admin
from ..forms import MedicationAdherenceForm
from ..models import MedicationAdherence
from .modeladmin import CrfModelAdmin


@admin.register(MedicationAdherence, site=effect_subject_admin)
class MedicationAdherenceAdmin(MedicationAdherenceAdminMixin, CrfModelAdmin):
    form = MedicationAdherenceForm
