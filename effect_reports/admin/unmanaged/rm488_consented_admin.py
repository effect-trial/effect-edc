from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from edc_dashboard.url_names import url_names
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.admin import QaReportWithNoteModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ...admin_site import effect_reports_admin
from ...models import Rm488Consented


@admin.register(Rm488Consented, site=effect_reports_admin)
class Rm488ConsentedAdmin(
    QaReportWithNoteModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    qa_report_list_display_insert_pos = 2
    change_list_note = format_html(
        "<p>Dynamic report listing summary of <strong>Subject Screening</strong> serum CrAg dates against eligibility dates "
        "where <em>current_sx_other</em> contains one or more of the "
        "following search terms:"
        "<ul>"
        "    <li>consti</li>"
        "    <li>diar</li>"
        "    <li>fatig</li>"
        "    <li>mala</li>"
        "    <li>weak</li>"
        "</ul>"
    )

    ordering = ["site", "subject_identifier"]

    list_display = [
        # "dashboard",
        "site",
        "screening",
        "initials",
        # "subject",
        # "age_sex",
        # "gender",
        # "eligibility_date",
        # "serum_crag_date",
        # "days_difference",
        # "confirmed_serum_crag_date",
        # "user_created",
        # "user_modified",
    ]

    list_filter = [
        ScheduleStatusListFilter,
        # "eligibility_date",
        # "serum_crag_date",
        # "days_difference",
        "site_id",
        # "user_created",
        # "user_modified",
        # "age_in_years",
        # "gender",
    ]

    # list_editable = ["confirmed_serum_crag_date"]

    search_fields = ["screening_identifier", "subject_identifier", "initials"]

    @admin.display(description="Screening", ordering="screening_identifier")
    def screening(self, obj):
        url_name = url_names.get("screening_listboard_url")
        url = reverse(
            url_name,
            kwargs={"screening_identifier": obj.screening_identifier},
        )
        return format_html("<a href='{}'>{}</a>", url, obj.screening_identifier)

        # @admin.display(description="Subject", ordering="subject_identifier")
        # def subject(self, obj):
        #     return obj.subject_identifier
        #
        # @admin.display(description="Age/Sex", ordering="age_in_years")
        # def age_sex(self, obj):
        #     return f"{obj.age_in_years} yrs {obj.gender}"
