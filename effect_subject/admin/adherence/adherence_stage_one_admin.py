from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import effect_subject_admin
from ...forms import AdherenceStageOneForm
from ...models import AdherenceStageOne
from ..fieldsets import (
    adherence_counselling_baseline_fieldset_tuple,
    adherence_narrative_fieldset_tuple,
)
from ..modeladmin import CrfModelAdmin
from ..radio_fields import adherence_counselling_baseline_radio_fields


@admin.register(AdherenceStageOne, site=effect_subject_admin)
class AdherenceStageOneAdmin(CrfModelAdmin):
    form = AdherenceStageOneForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        adherence_counselling_baseline_fieldset_tuple,
        adherence_narrative_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = adherence_counselling_baseline_radio_fields
