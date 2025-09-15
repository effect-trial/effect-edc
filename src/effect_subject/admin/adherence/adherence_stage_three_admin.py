from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import effect_subject_admin
from ...forms import AdherenceStageThreeForm
from ...models import AdherenceStageThree
from ..fieldsets import (
    adherence_counselling_fieldset_tuple,
    adherence_narrative_fieldset_tuple,
    medication_diary_review_fieldset_tuple,
    missed_doses_fieldset_tuple,
)
from ..modeladmin import CrfModelAdmin
from ..radio_fields import (
    adherence_counselling_radio_fields,
    missed_doses_radio_fields,
    pill_count_diary_review_radio_fields,
)
from .missed_doses_admin import FluconMissedDosesInline, FlucytMissedDosesInline


@admin.register(AdherenceStageThree, site=effect_subject_admin)
class AdherenceStageThreeAdmin(CrfModelAdmin):
    form = AdherenceStageThreeForm

    inlines = (
        FluconMissedDosesInline,
        FlucytMissedDosesInline,
    )

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        adherence_counselling_fieldset_tuple,
        (
            missed_doses_fieldset_tuple[0],
            missed_doses_fieldset_tuple[1]
            | {
                "description": (
                    "Missed doses must be checked against the participant's pill "
                    "count and adherence diary."
                ),
            },
        ),
        medication_diary_review_fieldset_tuple,
        adherence_narrative_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = (
        adherence_counselling_radio_fields
        | missed_doses_radio_fields
        | pill_count_diary_review_radio_fields
    )
