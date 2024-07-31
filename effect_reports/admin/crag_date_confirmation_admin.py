from django.contrib import admin
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.admin import QaReportWithNoteModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_reports_admin
from ..crag_date_df import CragDateDf
from ..models import CragDateConfirmation


@admin.register(CragDateConfirmation, site=effect_reports_admin)
class CragDateConfirmationAdmin(
    QaReportWithNoteModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    ordering = ("subject_identifier",)
    list_display = [
        "dashboard",
        "subject",
        "screening",
        "site",
        "report_date",
        "serum_crag_date",
        "serum_crag_value",
    ]

    list_filter = (
        "report_date",
        "serum_crag_date",
    )

    search_fields = [
        "screening_identifier",
        "subject_identifier",
    ]

    @admin.display(description="screening", ordering="screening_identifier")
    def screening(self, obj=None):
        return obj.screening_identifier

    @admin.display(description="subject", ordering="subject_identifier")
    def subject(self, obj=None):
        return obj.subject_identifier

    def get_queryset(self, request):
        cls = CragDateDf()
        cls.to_model()
        return super().get_queryset(request)
