from django.contrib import admin
from edc_model_admin.mixins import TabularInlineMixin

from ...forms import FluconMissedDosesForm, FlucytMissedDosesForm
from ...models import FluconMissedDoses, FlucytMissedDoses


class FluconMissedDosesInline(TabularInlineMixin, admin.TabularInline):
    model = FluconMissedDoses
    form = FluconMissedDosesForm
    extra = 1
    view_on_site = False

    fieldsets = (
        [
            "Missed fluconazole doses",
            {
                "fields": (
                    "day_missed",
                    "missed_reason",
                    "missed_reason_other",
                )
            },
        ],
    )


class FlucytMissedDosesInline(TabularInlineMixin, admin.TabularInline):
    model = FlucytMissedDoses
    form = FlucytMissedDosesForm
    extra = 1
    view_on_site = False

    fieldsets = (
        [
            "Missed flucytosine doses",
            {
                "fields": (
                    "day_missed",
                    "doses_missed",
                    "missed_reason",
                    "missed_reason_other",
                )
            },
        ],
    )
