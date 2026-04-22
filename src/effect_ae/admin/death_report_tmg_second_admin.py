from django.contrib import admin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_ae_admin
from ..forms import DeathReportTmgSecondForm
from ..models import DeathReportTmgSecond
from .modeladmin_mixins import DeathReportTmgModelAdminMixin


@admin.register(DeathReportTmgSecond, site=effect_ae_admin)
class DeathReportTmgSecondAdmin(
    SiteModelAdminMixin,
    DeathReportTmgModelAdminMixin,
    SimpleHistoryAdmin,
):
    form = DeathReportTmgSecondForm

    def get_view_only_site_ids_for_user(self, request) -> list[int]:
        return [s.id for s in request.user.userprofile.sites.all() if s.id != request.site.id]

    def user_may_view_other_sites(self, request) -> bool:  # noqa: ARG002
        return True
