from clinicedc_constants import NOT_EVALUATED
from django.db import models
from edc_adverse_event.model_mixins import DeathReportTmgModelMixin
from edc_model.models import BaseUuidModel

from ..choices import CRYPTOCOCCAL_RELATIONSHIP


class DeathReportTmg(DeathReportTmgModelMixin, BaseUuidModel):
    cryptococcal_relatedness = models.CharField(
        verbose_name="In your opinion, is the cause death related to cryptococcal infection?",
        max_length=25,
        choices=CRYPTOCOCCAL_RELATIONSHIP,
        default=NOT_EVALUATED,
    )

    class Meta(DeathReportTmgModelMixin.Meta, BaseUuidModel.Meta):
        pass
