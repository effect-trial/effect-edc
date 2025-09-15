from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import effect_subject_admin
from ...forms import AdherenceForm
from ...models import Adherence
from ..fieldsets import (
    adherence_counselling_baseline_fieldset_tuple,
    adherence_summary_fieldset_tuple,
    medication_diary_review_fieldset_tuple,
    missed_doses_fieldset_tuple,
)
from ..modeladmin import CrfModelAdmin
from ..radio_fields import (
    adherence_counselling_baseline_radio_fields,
    adherence_summary_radio_fields,
    missed_doses_radio_fields,
    pill_count_diary_review_radio_fields,
)


@admin.register(Adherence, site=effect_subject_admin)
class AdherenceAdmin(CrfModelAdmin):
    form = AdherenceForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        adherence_counselling_baseline_fieldset_tuple,
        missed_doses_fieldset_tuple,
        medication_diary_review_fieldset_tuple,
        adherence_summary_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = (
        adherence_counselling_baseline_radio_fields
        | missed_doses_radio_fields
        | pill_count_diary_review_radio_fields
        | adherence_summary_radio_fields
    )
