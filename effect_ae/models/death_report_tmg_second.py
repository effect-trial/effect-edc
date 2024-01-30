from edc_adverse_event.model_mixins import DeathReportTmgSecondModelMixin
from edc_model.models import BaseUuidModel


class DeathReportTmgSecond(DeathReportTmgSecondModelMixin, BaseUuidModel):
    class Meta(DeathReportTmgSecondModelMixin.Meta, BaseUuidModel.Meta):
        pass
