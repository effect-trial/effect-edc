from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_model.validators import date_not_future

from effect_lists.models import Medication, TbTreatments

from ..choices import FLUCONAZOLE_DOSES, TB_SITE_CHOICES, TB_TX_TYPES
from ..model_mixins import CrfModelMixin


class ParticipantHistory(CrfModelMixin, edc_models.BaseUuidModel):

    flucon_1w_prior_rando = models.CharField(
        verbose_name="Fluconazole taken within 1 week prior to randomization?",
        max_length=5,
        choices=YES_NO,
    )

    flucon_days = models.IntegerField(
        verbose_name="If YES, number of days Fluconazole taken:",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )

    flucon_dose = models.CharField(
        verbose_name="If YES, Fluconazole dose (if taken < 1 week prior to randomisation):",
        max_length=25,
        choices=FLUCONAZOLE_DOSES,
        help_text="in mg/d",
    )

    flucon_dose_other = models.IntegerField(
        verbose_name="Other Fluconazole dose (if taken < 1 week prior to randomisation):",
        validators=[MinValueValidator(1), MaxValueValidator(1199)],
        null=True,
        blank=True,
        help_text="in mg/d",
    )

    flucon_dose_other_reason = edc_models.OtherCharField(
        verbose_name="Other Fluconazole dose reason:"
    )

    reported_neuro_abnormality = models.CharField(
        verbose_name=(
            "Is there any reported neurological abnormality "
            "following examination by a medical practitioner?"
        ),
        max_length=5,
        choices=YES_NO,
        help_text="Must be confirmed as not related to CM",
    )

    neuro_abnormality_details = models.TextField(
        verbose_name="Details of neurological abnormality?",
        null=True,
        blank=True,
    )

    tb_prev_dx = models.CharField(
        verbose_name="Previous diagnosis of Tuberculosis?",
        max_length=5,
        choices=YES_NO,
    )

    tb_dx_date = models.DateField(
        verbose_name="If YES, give date",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    tb_dx_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If YES, is this date estimated?", default=NOT_APPLICABLE
    )

    tb_site = models.CharField(
        verbose_name="If YES, site of TB?",
        max_length=15,
        choices=TB_SITE_CHOICES,
        default=NOT_APPLICABLE,
    )

    on_tb_tx = models.CharField(
        verbose_name="Is the participant currently taking TB treatment?",
        max_length=5,
        choices=YES_NO,
    )

    tb_tx_type = models.CharField(
        verbose_name="If YES, please specify type?",
        max_length=15,
        choices=TB_TX_TYPES,
        default=NOT_APPLICABLE,
        help_text="If 'Active TB' please specify treatment below ...",
    )

    active_tb_tx = models.ManyToManyField(
        TbTreatments,
        verbose_name="If 'Active TB', which treatment?",
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

    any_medications = models.CharField(
        verbose_name="Other medication?", max_length=5, choices=YES_NO
    )

    specify_medications = models.ManyToManyField(Medication, blank=True)

    specify_steroid_other = models.TextField(
        verbose_name="If STEROID, specify type and dose of steroid ...",
        max_length=150,
        blank=True,
        null=True,
    )

    specify_medications_other = models.TextField(
        verbose_name="If OTHER, specify ...", max_length=150, blank=True, null=True
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Participant History"
        verbose_name_plural = "Participant History"
