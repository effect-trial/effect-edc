from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class HealthEconomicsBaseline(CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Health Economics: Baseline"
        verbose_name_plural = "Health Economics: Baseline"


# TODO: this HEALTH ECONOMICS always required at unscheduled visits and SAE
class HealthEconomics(CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Health Economics"
        verbose_name_plural = "Health Economics"


# TODO: this HEALTH ECONOMICS only at 24m or always with EoS CRF
class HealthEconomicsEnd(CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Health Economics: End of Study"
        verbose_name_plural = "Health Economics"
