from edc_adverse_event.model_mixins import DeathReportTmgSecondModelMixin

from effect_ae.models import DeathReportTmg


class DeathReportTmgSecond(DeathReportTmgSecondModelMixin, DeathReportTmg):
    class Meta(DeathReportTmgSecondModelMixin.Meta):
        proxy = True
