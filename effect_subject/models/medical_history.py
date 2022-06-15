from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class MedicalHistory(CrfModelMixin, edc_models.BaseUuidModel):
    class Meta(CrfModelMixin.Meta):
        verbose_name = "Medical History"
        verbose_name_plural = "Medical History"
