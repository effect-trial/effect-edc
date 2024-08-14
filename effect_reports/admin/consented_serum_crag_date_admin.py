from django.apps import apps as django_apps
from django.contrib import admin
from django.utils.html import format_html
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.admin import NoteModelAdminMixin
from edc_qareports.utils import truncate_string
from edc_sites.admin import SiteModelAdminMixin
from edc_utils import escape_braces

from ..admin_site import effect_reports_admin
from ..consented_serum_crag_date_df import ConsentedSerumCragDateDf
from ..models import ConsentedSerumCragDate


@admin.register(ConsentedSerumCragDate, site=effect_reports_admin)
class ConsentedSerumCragDateAdmin(
    NoteModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    qa_report_list_display_insert_pos = 5

    note_model_cls = django_apps.get_model("effect_reports.confirmedserumcragdate")

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

    @admin.display(description="Conf. ser CrAg Date")
    def notes(self, obj=None):
        """Returns url to add or edit qa_report model note"""
        return super().notes(obj=obj)

    def get_notes_label(self, obj=None, field_name=None):
        if not obj:
            label = "Add"
        else:
            date = obj.confirmed_serum_crag_date
            note = obj.note
            if date and not note:
                label = date
            elif date and note:
                label = format_html(
                    f"{date.strftime('%-d %b %Y')}<br>"
                    f"({escape_braces(truncate_string(note, max_length=35))})"
                )
            elif note:
                label = truncate_string(note, max_length=35)
            else:
                label = "Edit"
        return label

    def get_queryset(self, request):
        cls = ConsentedSerumCragDateDf()
        cls.to_model()
        return super().get_queryset(request)
