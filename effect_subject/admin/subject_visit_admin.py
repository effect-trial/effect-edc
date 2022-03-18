from django.contrib import admin
from edc_model_admin import SimpleHistoryAdmin, audit_fieldset_tuple
from edc_visit_schedule.fieldsets import visit_schedule_fieldset_tuple
from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from ..admin_site import effect_subject_admin
from ..forms import SubjectVisitForm
from ..models import SubjectVisit
from .modeladmin import ModelAdminMixin


@admin.register(SubjectVisit, site=effect_subject_admin)
class SubjectVisitAdmin(VisitModelAdminMixin, ModelAdminMixin, SimpleHistoryAdmin):

    show_dashboard_in_list_display_pos = 2

    form = SubjectVisitForm

    fieldsets = (
        (
            None,
            {
                "fields": [
                    "appointment",
                    "report_datetime",
                    "reason",
                    "reason_unscheduled",
                    "reason_unscheduled_other",
                ]
            },
        ),
        (
            "Information source",
            {
                "fields": (
                    "assessment_type",
                    "assessment_type_other",
                    "assessment_who",
                    "assessment_who_other",
                    "info_source",
                    "info_source_other",
                )
            },
        ),
        (
            "Patient status",
            {
                "fields": (
                    "survival_status",
                    "last_alive_date",
                    "hospitalized",
                )
            },
        ),
        ("Comments", {"fields": ("comments",)}),
        visit_schedule_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {
        "assessment_type": admin.VERTICAL,
        "assessment_who": admin.VERTICAL,
        "hospitalized": admin.VERTICAL,
        "info_source": admin.VERTICAL,
        "reason": admin.VERTICAL,
        "reason_unscheduled": admin.VERTICAL,
        "survival_status": admin.VERTICAL,
    }
