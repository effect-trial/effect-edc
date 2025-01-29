from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ...admin_site import effect_reports_admin
from ...modeladmin_mixins import CrfReportModelAdminMixin, EffectReportModelAdminMixin
from ...models import Rm792KwInCurrentSxGteG3Other


@admin.register(Rm792KwInCurrentSxGteG3Other, site=effect_reports_admin)
class Rm792KwInCurrentSxGteG3OtherAdmin(
    CrfReportModelAdminMixin,
    EffectReportModelAdminMixin,
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    crf_model = "effect_subject.signsandsymptoms"
    qa_report_list_display_insert_pos = 4
    site_list_display_insert_pos = 2
    list_per_page = 25

    change_list_note = format_html(
        "{html}",
        html=mark_safe(
            render_to_string(
                "effect_reports/rm792_kw_in_sx_other/changelist_note.html",
                context=dict(other_field="current_sx_gte_g3_other"),
            )
        ),  # nosec #B703 # B308
    )

    ordering = ["site", "subject_identifier", "visit_code", "visit_code_sequence"]

    list_display = [
        "subject_dashboard",
        "visit_dashboard",
        "site",
        "update_crf",
        "current_sx_gte_g3_other",
        "user_created",
        "user_modified",
        "modified",
    ]

    list_filter = [
        ScheduleStatusListFilter,
        "visit_code",
        "visit_code_sequence",
        "site_id",
        "user_created",
        "user_modified",
    ]

    search_fields = ["subject_identifier", "current_sx_gte_g3_other"]
