from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_model.validators import date_not_future

from ..choices import TB_DX_AGO_CHOICES, TB_SITE_CHOICES
from ..model_mixins import CrfModelMixin


class MedicalHistory(CrfModelMixin, edc_models.BaseUuidModel):

    tb_prev_dx = models.CharField(
        verbose_name="Previous diagnosis of Tuberculosis?",
        max_length=5,
        choices=YES_NO,
    )

    tb_site = models.CharField(
        verbose_name="If YES, site of TB?",
        max_length=15,
        choices=TB_SITE_CHOICES,
        default=NOT_APPLICABLE,
    )

    on_tb_tx = models.CharField(
        verbose_name="Are you currently taking TB treatment?",
        max_length=5,
        choices=YES_NO_NA,
    )

    tb_dx_ago = models.CharField(
        verbose_name="If NO, when was TB diagnosis?",
        max_length=15,
        choices=TB_DX_AGO_CHOICES,
        default=NOT_APPLICABLE,
    )

    on_rifampicin = models.CharField(
        verbose_name="If YES, are you currently also taking Rifampicin?",
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    rifampicin_start_date = models.DateField(
        verbose_name="If YES, when did you first start taking Rifampicin?",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    previous_oi = models.CharField(
        verbose_name="Previous opportunistic infection other than TB?",
        max_length=5,
        choices=YES_NO,
    )

    previous_oi_name = edc_models.OtherCharField(
        verbose_name="If YES, specify opportunistic infection name?"
    )

    previous_oi_dx_date = models.DateField(
        verbose_name=(
            "If YES, what was the date of the previous opportunistic infection diagnosis?"
        ),
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Medical History"
        verbose_name_plural = "Medical History"
