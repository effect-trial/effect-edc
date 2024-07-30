from django.contrib import admin
from django.utils.html import format_html
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from ...admin_site import effect_reports_admin
from ...models import Rm792SiSxListCandidates


@admin.register(Rm792SiSxListCandidates, site=effect_reports_admin)
class Rm792SiSxListCandidatesAdmin(
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    change_list_note = format_html(
        "<p>Dynamic report listing <strong>Signs and Symptoms</strong> CRFs "
        "where <em>current_sx_other</em> contains one or more of the "
        "following search terms:"
        "<ul>"
        "    <li>appet</li>"
        "    <li>abdom</li>"
        "    <li>back</li>"
        "    <li>conf</li>"
        "    <li>diz</li>"
        "    <li>itchy</li>"
        "    <li>rash</li>"
        "    <li>pleur</li>"
        "</ul>"
    )

    ordering = ["current_sx_other", "site"]

    list_display = ["current_sx_other", "site"]

    list_filter = ["current_sx_other", "site"]

    search_fields = ["current_sx_other"]
