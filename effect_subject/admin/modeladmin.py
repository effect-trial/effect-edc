from edc_action_item import ActionItemModelAdminMixin
from edc_model_admin.dashboard import (
    ModelAdminCrfDashboardMixin,
    ModelAdminSubjectDashboardMixin,
)
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin


class ModelAdminMixin(SiteModelAdminMixin, ModelAdminSubjectDashboardMixin):
    pass


class CrfWithActionModelAdmin(
    SiteModelAdminMixin,
    ModelAdminCrfDashboardMixin,
    ActionItemModelAdminMixin,
    SimpleHistoryAdmin,
):
    pass


class CrfModelAdmin(
    SiteModelAdminMixin,
    ModelAdminCrfDashboardMixin,
    SimpleHistoryAdmin,
):
    pass
