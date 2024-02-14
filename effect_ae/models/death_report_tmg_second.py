from edc_adverse_event.constants import DEATH_REPORT_TMG_SECOND_ACTION
from edc_adverse_event.model_mixins import (
    DeathReportTmgSecondManager,
    DeathReportTmgSecondModelMixin,
    DeathReportTmgSecondSiteManager,
)

from effect_ae.models import DeathReportTmg


class DeathReportTmgSecond(DeathReportTmgSecondModelMixin, DeathReportTmg):
    action_name = DEATH_REPORT_TMG_SECOND_ACTION

    objects = DeathReportTmgSecondManager()

    on_site = DeathReportTmgSecondSiteManager()

    class Meta(DeathReportTmgSecondModelMixin.Meta):
        proxy = True
