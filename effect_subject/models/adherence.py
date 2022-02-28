from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class Adherence(CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Adherence"
        verbose_name_plural = "Adherence"
