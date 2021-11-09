from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_model import models as edc_models

from effect_lists.models import XRayResults

from ..model_mixins import CrfModelMixin


class ChestXray(CrfModelMixin, edc_models.BaseUuidModel):

    chest_xray = models.CharField(
        verbose_name="Has a chest x-ray been carried out?",
        max_length=15,
        choices=YES_NO,
    )

    chest_xray_date = models.DateField(
        verbose_name="If yes, what date was it performed?",
        null=True,
        blank=True,
    )

    chest_xray_results = models.ManyToManyField(
        XRayResults,
        verbose_name="Chest x-ray result",
        blank=True,
    )

    comment = models.TextField(
        verbose_name="Any additional comment", null=True, blank=True
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Chest X-ray"
        verbose_name_plural = "Chest X-ray"
