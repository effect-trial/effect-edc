from edc_microbiology.model_mixins import (
    BloodCultureModelMixin,
    CsfModelMixin,
    HistopathologyModelMixin,
    SputumModelMixin,
    UrineCultureModelMixin,
)
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class Microbiology(
    UrineCultureModelMixin,
    BloodCultureModelMixin,
    SputumModelMixin,
    CsfModelMixin,
    HistopathologyModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):
    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Microbiology"
        verbose_name_plural = "Microbiology"
