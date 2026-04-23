from clinicedc_constants import NOT_EVALUATED, NULL_STRING
from django.db import models
from edc_action_item.managers import ActionIdentifierModelManager, ActionIdentifierSiteManager
from edc_adverse_event.constants import DEATH_REPORT_TMG_SECOND_ACTION
from edc_adverse_event.model_mixins import DeathReportTmgModelMixin
from edc_model.models import BaseUuidModel

from ..choices import CRYPTOCOCCAL_RELATIONSHIP


class DeathReportTmgSecondManager(ActionIdentifierModelManager):
    pass


class DeathReportTmgSecond(DeathReportTmgModelMixin, BaseUuidModel):
    action_name = DEATH_REPORT_TMG_SECOND_ACTION

    cryptococcal_relatedness = models.CharField(
        verbose_name="In your opinion, is the cause death related to cryptococcal infection?",
        max_length=25,
        choices=CRYPTOCOCCAL_RELATIONSHIP,
        default=NOT_EVALUATED,
    )

    cryptococcal_relatedness_comment = models.TextField(
        max_length=250, default=NULL_STRING, blank=True
    )

    objects = DeathReportTmgSecondManager()

    on_site = ActionIdentifierSiteManager()

    class Meta(DeathReportTmgModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Death Report TMG (2nd)"
        verbose_name_plural = "Death Report TMG (2nd)"
