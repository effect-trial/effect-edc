from django.db import models
from django.db.models import PROTECT
from edc_lab.utils import get_requisition_model_name
from edc_microbiology.model_mixins import BloodCultureModelMixin
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class BloodCulture(BloodCultureModelMixin, CrfModelMixin, edc_models.BaseUuidModel):
    requisition = models.ForeignKey(
        get_requisition_model_name(),
        on_delete=PROTECT,
        related_name="+",
        verbose_name="Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit",
    )

    comment = models.TextField(verbose_name="Any additional comment", null=True, blank=True)

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Blood Culture"
        verbose_name_plural = "Blood Culture"
