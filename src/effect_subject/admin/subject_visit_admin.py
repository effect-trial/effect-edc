from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django_audit_fields.admin import audit_fieldset_tuple
from edc_appointment.models import Appointment
from edc_constants.constants import IN_PERSON, NO, PATIENT
from edc_document_status.fieldsets import document_status_fieldset_tuple
from edc_model_admin.history import SimpleHistoryAdmin
from edc_visit_schedule.constants import DAY1
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
                ],
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
                ),
            },
        ),
        (
            "Participant status",
            {
                "fields": (
                    "survival_status",
                    "last_alive_date",
                    "hospitalized",
                ),
            },
        ),
        ("Comments", {"fields": ("comments",)}),
        visit_schedule_fieldset_tuple,
        document_status_fieldset_tuple,
        audit_fieldset_tuple,
    )

    radio_fields = {  # noqa: RUF012
        "assessment_type": admin.VERTICAL,
        "assessment_who": admin.VERTICAL,
        "hospitalized": admin.VERTICAL,
        "info_source": admin.VERTICAL,
        "reason": admin.VERTICAL,
        "reason_unscheduled": admin.VERTICAL,
        "survival_status": admin.VERTICAL,
    }

    def get_changeform_initial_data(self, request):
        # TODO: this could be more predictive for non-baseline visits
        initial_data = super().get_changeform_initial_data(request)
        appointment_id = request.GET.get("appointment")
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except ObjectDoesNotExist:
            pass
        else:
            initial_data.update(
                assessment_type=IN_PERSON if appointment.visit_code == DAY1 else None,
                assessment_who=PATIENT if appointment.visit_code == DAY1 else None,
                info_source=PATIENT if appointment.visit_code == DAY1 else None,
                hospitalized=NO if appointment.visit_code == DAY1 else None,
            )
        return initial_data
