from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import effect_subject_admin
from ...forms import AdherenceStageFourForm
from ...models import AdherenceStageFour
from ..fieldsets import (
    adherence_counselling_fieldset_tuple,
    adherence_summary_fieldset_tuple,
)
from ..modeladmin import CrfModelAdmin
from ..radio_fields import (
    adherence_counselling_radio_fields,
    adherence_summary_radio_fields,
)


@admin.register(AdherenceStageFour, site=effect_subject_admin)
class AdherenceStageFourAdmin(CrfModelAdmin):
    form = AdherenceStageFourForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        adherence_counselling_fieldset_tuple,
        adherence_summary_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = adherence_counselling_radio_fields | adherence_summary_radio_fields
