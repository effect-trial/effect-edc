from django.db import models
from django.db.models import PROTECT
from edc_constants.choices import YES_NO
from edc_csf.model_mixins import (
    CsfCultureModelMixin,
    CsfModelMixin,
    LpModelMixin,
    QuantitativeCultureModelMixin,
)
from edc_lab.utils import get_requisition_model_name
from edc_model import models as edc_models

from ..choices import LP_REASON
from ..model_mixins import CrfModelMixin


class LpCsf(
    LpModelMixin,
    CsfModelMixin,
    CsfCultureModelMixin,
    QuantitativeCultureModelMixin,
    CrfModelMixin,
    edc_models.BaseUuidModel,
):
    lp_done = models.CharField(
        verbose_name="Was LP done?",
        max_length=15,
        choices=YES_NO,
        blank=False,
    )

    # overrides from LpModelMixin
    reason_for_lp = models.CharField(
        verbose_name="Reason for LP", max_length=50, choices=LP_REASON
    )

    csf_requisition = models.ForeignKey(
        get_requisition_model_name(),
        on_delete=PROTECT,
        related_name="csfrequisition",
        verbose_name="CSF Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Lumbar Puncture/CSF"
        verbose_name_plural = "Lumbar Puncture/CSF"
