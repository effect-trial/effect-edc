from django.contrib import admin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_prn_admin
from ..models import OnSchedule


@admin.register(OnSchedule, site=effect_prn_admin)
class OnScheduleAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    instructions = None

    fields = ("subject_identifier", "onschedule_datetime")

    list_display = ("subject_identifier", "dashboard", "onschedule_datetime")

    list_filter = ("onschedule_datetime",)

    def get_readonly_fields(self, request, obj=None) -> tuple[str, ...]:  # noqa: ARG002
        return ("onschedule_datetime",)
