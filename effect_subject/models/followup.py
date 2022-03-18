from django.db import models
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models

from ..constants import FOLLOWUP_ACTION


class Followup(CrfWithActionModelMixin, edc_models.BaseUuidModel):

    action_name = FOLLOWUP_ACTION

    tracking_identifier_prefix = "FU"

    action_identifier = models.CharField(max_length=50, unique=True, null=True)

    tracking_identifier = models.CharField(max_length=30, unique=True, null=True)

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Follow-up"
        verbose_name_plural = "Follow-up"
