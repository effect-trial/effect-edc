from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from effect_lists.models import XRayResults

from ..model_mixins import CrfModelMixin


class ChestXray(CrfModelMixin, edc_models.BaseUuidModel):

    chest_xray = models.CharField(
        verbose_name="Was a chest x-ray performed?",
        max_length=15,
        choices=YES_NO,
    )

    chest_xray_date = models.DateField(
        verbose_name="If YES, date performed?",
        null=True,
        blank=True,
    )

    chest_xray_results = models.ManyToManyField(
        XRayResults,
        verbose_name="If YES, indicate results?",
        blank=True,
    )

    chest_xray_results_other = models.TextField(
        verbose_name="If other, please specify ...",
        null=True,
        blank=True,
    )

    comment = models.TextField(verbose_name="Any additional comment", null=True, blank=True)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Chest X-ray"
        verbose_name_plural = "Chest X-rays"
