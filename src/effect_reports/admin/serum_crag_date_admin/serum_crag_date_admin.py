from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_utils import escape_braces, truncate_string

from ...admin_site import effect_reports_admin
from ...dataframes import SerumCragDateDf
from ...modeladmin_mixins import EffectReportModelAdminMixin
from ...models import SerumCragDate
from .list_filters import SerumCragDateNoteStatusListFilter


@admin.register(SerumCragDate, site=effect_reports_admin)
class SerumCragDateAdmin(
    EffectReportModelAdminMixin,
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    qa_report_list_display_insert_pos = 4
    site_list_display_insert_pos = 1
    list_per_page = 25
    note_model = "effect_reports.serumcragdatenote"
    note_status_list_filter = SerumCragDateNoteStatusListFilter

    ordering = ("subject_identifier",)
    list_display = (
        "subject_dashboard",
        "site",
        "screening",
        "serum_crag_date",
        "eligibility_date",
        "serum_crag_value",
    )

    list_filter = (
        "serum_crag_date",
        "eligibility_date",
        "serum_crag_value",
        "site",
    )

    search_fields = (
        "screening_identifier",
        "subject_identifier",
    )

    @admin.display(description="screening", ordering="screening_identifier")
    def screening(self, obj=None):
        return obj.screening_identifier

    @admin.display(description="subject", ordering="subject_identifier")
    def subject(self, obj=None):
        return obj.subject_identifier

    @admin.display(description="Confirm")
    def notes(self, obj=None):
        """Overridden to change description"""
        return super().notes(obj=obj)

    def get_notes_label(self, obj=None, field_name=None):  # noqa: ARG002
        if not obj:
            label = _("Add")
        else:
            date = obj.serum_crag_date
            note = obj.note
            if date and not note:
                label = date
            elif date and note:
                label = format_html(
                    "{html}",
                    html=mark_safe(  # noqa: S308
                        f"{date.strftime('%-d %b %Y')}<br>"
                        f"({escape_braces(truncate_string(note, max_length=35))})",
                    ),
                )
            elif note:
                label = truncate_string(note, max_length=35)
            else:
                label = _("Edit")
        return label

    def get_queryset(self, request):
        df_cls = SerumCragDateDf()
        df_cls.to_model()
        return super().get_queryset(request)
