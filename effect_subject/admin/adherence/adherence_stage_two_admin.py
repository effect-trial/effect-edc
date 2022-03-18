from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import effect_subject_admin
from ...forms import AdherenceStageTwoForm
from ...models import AdherenceStageTwo
from ..fieldsets import (
    adherence_counselling_fieldset_tuple,
    adherence_narrative_fieldset_tuple,
    missed_doses_fieldset_tuple,
)
from ..modeladmin import CrfModelAdmin
from ..radio_fields import adherence_counselling_radio_fields, missed_doses_radio_fields


@admin.register(AdherenceStageTwo, site=effect_subject_admin)
class AdherenceStageTwoAdmin(CrfModelAdmin):

    form = AdherenceStageTwoForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        adherence_counselling_fieldset_tuple,
        missed_doses_fieldset_tuple,
        adherence_narrative_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = adherence_counselling_radio_fields | missed_doses_radio_fields
