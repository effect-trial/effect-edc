from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_adverse_event.modeladmin_mixins import DeathReportModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import effect_ae_admin
from ..forms import DeathReportForm
from ..models import DeathReport


@admin.register(DeathReport, site=effect_ae_admin)
class DeathReportAdmin(DeathReportModelAdminMixin, SimpleHistoryAdmin):

    form = DeathReportForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject_identifier",
                    "report_datetime",
                )
            },
        ),
        (
            "Death",
            {"fields": ("death_datetime",)},
        ),
        (
            "Hospitalization",
            {
                "fields": (
                    "death_as_inpatient",
                    "hospitalization_date",
                    "hospitalization_date_estimated",
                    "clinical_notes_available",
                    "cm_sx",
                )
            },
        ),
        (
            "Next of kin",
            {
                "fields": (
                    "speak_nok",
                    "date_first_unwell",
                    "date_first_unwell_estimated",
                    "headache",
                    "drowsy_confused_altered_behaviour",
                    "seizures",
                    "nok_narrative",
                )
            },
        ),
        (
            "Opinion of Local Study Doctor and Local PI",
            {"fields": ("cause_of_death", "cause_of_death_other", "narrative")},
        ),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "cause_of_death": admin.VERTICAL,
        "clinical_notes_available": admin.VERTICAL,
        "cm_sx": admin.VERTICAL,
        "date_first_unwell_estimated": admin.VERTICAL,
        "death_as_inpatient": admin.VERTICAL,
        "drowsy_confused_altered_behaviour": admin.VERTICAL,
        "headache": admin.VERTICAL,
        "hospitalization_date_estimated": admin.VERTICAL,
        "seizures": admin.VERTICAL,
        "speak_nok": admin.VERTICAL,
    }
