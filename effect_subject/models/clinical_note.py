from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class ClinicalNote(CrfModelMixin, edc_models.BaseUuidModel):

    has_comment = models.CharField(
        verbose_name="Are there any comments on the clinical care or assessment plan",
        max_length=15,
        choices=YES_NO,
    )

    # TODO: Ask on every visit
    # TODO: Encrypt
    comments = models.TextField(verbose_name="Comments", null=True, blank=True)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Clinical Note"
        verbose_name_plural = "Clinical Note"
