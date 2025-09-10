from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from . import CrfReportModelAdminMixin, EffectReportModelAdminMixin


class BaselineVlModelAdminMixin(
    CrfReportModelAdminMixin,
    EffectReportModelAdminMixin,
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
):
    report_model: str = None
    crf_model = "effect_subject.arvhistory"
    qa_report_list_display_insert_pos = 4
    site_list_display_insert_pos: int = 2
    ordering = ["site", "subject_identifier"]

    list_display = [
        "subject_dashboard",
        "visit_dashboard",
        "site",
        "update_crf",
        "has_viral_load_result",
        "viral_load_result",
        "viral_load_quantifier",
        "viral_load_date",
        "viral_load_date_estimated",
        "user_created",
        "user_modified",
        "created",
        "modified",
    ]

    list_filter = (
        "has_viral_load_result",
        "viral_load_result",
        "viral_load_quantifier",
        "viral_load_date",
        "viral_load_date_estimated",
        "site_id",
        "user_created",
        "user_modified",
        "created",
        "modified",
    )

    search_fields = [
        "subject_identifier",
        "viral_load_result",
    ]
