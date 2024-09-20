from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from edc_appointment.models import Appointment
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin
from edc_visit_schedule.admin import ScheduleStatusListFilter

from ...admin_site import effect_reports_admin
from ...models import Rm792KwInCurrentSxGteG3Other


@admin.register(Rm792KwInCurrentSxGteG3Other, site=effect_reports_admin)
class Rm792KwInCurrentSxGteG3OtherAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    list_per_page = 25
    change_list_note = format_html(
        "<p>Dynamic report listing <strong>Signs and Symptoms</strong> CRFs "
        "where <em>current_sx_gte_g3_other</em> contains one or more of the "
        "following search terms:"
        "<ul style='columns: 3; -webkit-columns: 3; -moz-columns: 3; max-width: 250px;'>"
        "    <li>abdom</li>"
        "    <li>appet</li>"
        "    <li>back</li>"
        "    <li>behav</li>"
        "    <li>conf</li>"
        "    <li>consti</li>"
        "    <li>diar</li>"
        "    <li>diz</li>"
        "    <li>fatig</li>"
        "    <li>itchy</li>"
        "    <li>mala</li>"
        "    <li>neuro</li>"
        "    <li>pleur</li>"
        "    <li>rash</li>"
        "    <li>urin</li>"
        "    <li>weak</li>"
        "</ul>"
    )

    ordering = ["site", "subject_identifier", "visit_code", "visit_code_sequence"]

    list_display = [
        "dashboard",
        "site",
        "subject_identifier",
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

    def dashboard(self, obj=None, label=None) -> str:
        kwargs = self.get_subject_dashboard_url_kwargs(obj)
        try:
            kwargs.update(
                appointment=str(
                    Appointment.objects.get(
                        subject_identifier=obj.subject_identifier,
                        visit_code=obj.visit_code,
                        visit_code_sequence=obj.visit_code_sequence,
                    ).id
                )
            )
        except ObjectDoesNotExist:
            pass
        url = reverse(self.get_subject_dashboard_url_name(obj=obj), kwargs=kwargs)
        context = dict(
            title=_(f"Go to subject's dashboard@{obj.visit_code}.{obj.visit_code_sequence}"),
            url=url,
            label=_(f"Visit: {obj.visit_code}.{obj.visit_code_sequence}"),
        )
        return render_to_string("dashboard_button.html", context=context)
