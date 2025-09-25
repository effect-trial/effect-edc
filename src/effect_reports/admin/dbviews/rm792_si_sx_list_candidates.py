from django.contrib import admin
from django.template.loader import render_to_string
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
    change_list_note = render_to_string(
        "effect_reports/rm792_kw_in_sx_other/changelist_note.html",
        context=dict(other_field="current_sx_other"),
    )

    ordering = (
        "current_sx_other",
        "site",
    )

    list_display = (
        "current_sx_other",
        "site",
    )

    list_filter = (
        "current_sx_other",
        "site",
    )

    search_fields = ("current_sx_other",)
