from django.db import models
from edc_constants.choices import YES_NO
from edc_csf.model_mixins import (
    CsfCultureModelMixin,
    CsfModelMixin,
    LpModelMixin,
    QuantitativeCultureModelMixin,
)
from edc_lab.model_mixins import requisition_fk_options
from edc_model import models as edc_models

from effect_labs.panels import csf_culture_panel

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
        related_name="csfrequisition",
        verbose_name="CSF Requisition",
        limit_choices_to={"panel__name": csf_culture_panel.name},
        **{
            k: v
            for k, v in requisition_fk_options.items()
            if k not in ["related_name", "verbose_name"]
        },
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Lumbar Puncture/CSF"
        verbose_name_plural = "Lumbar Puncture/CSF"
