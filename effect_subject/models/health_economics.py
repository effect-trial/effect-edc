from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class HealthEconomics(CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Health Economics"
        verbose_name_plural = "Health Economics"
