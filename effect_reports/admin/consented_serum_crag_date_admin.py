from django.contrib import admin
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.admin import QaReportWithNoteModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_reports_admin
from ..consented_serum_crag_date_df import ConsentedSerumCragDateDf
from ..models import ConsentedSerumCragDate


@admin.register(ConsentedSerumCragDate, site=effect_reports_admin)
class ConsentedSerumCragDateAdmin(
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
        "serum_crag_date",
        "eligibility_date",
        "serum_crag_value",
    ]

    list_filter = (
        "serum_crag_date",
        "eligibility_date",
        "serum_crag_value",
        "site",
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
        cls = ConsentedSerumCragDateDf()
        cls.to_model()
        return super().get_queryset(request)
