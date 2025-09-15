from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_model.validators import date_not_future

from effect_lists.models import Antibiotics, Drugs, TbTreatments
from effect_subject.choices import CM_TX_CHOICES, NEGATIVE_TX_CHOICES, STEROID_CHOICES

from ..model_mixins import CrfModelMixin


class ParticipantTreatment(CrfModelMixin, edc_models.BaseUuidModel):
    # Participant Treatment CRF (p4)
    lp_completed = models.CharField(
        verbose_name="LP completed?",
        max_length=15,
        # TODO: If yes, prompt for lab results
        choices=YES_NO,
        help_text="If YES, complete laboratory results",
    )

    cm_confirmed = models.CharField(
        verbose_name="Cryptococcal meningitis confirmed?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    on_cm_tx = models.CharField(
        verbose_name="Cryptococcal meningitis treatment administered?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    cm_tx_given = models.CharField(
        verbose_name="If YES, treatment given?",
        max_length=15,
        choices=CM_TX_CHOICES,
        default=NOT_APPLICABLE,
    )

    cm_tx_given_other = edc_models.OtherCharField()

    on_tb_tx = models.CharField(
        verbose_name="Has the participant been put on TB preventive therapy?",
        max_length=15,
        choices=YES_NO,
        help_text=(
            "Select NO if started pre-enrolment or on day 1, and captured on day 1. "
            "Select YES if started today."
        ),
    )

    tb_tx_date = models.DateField(
        verbose_name="If YES, give date",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    tb_tx_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If YES, is this date estimated?",
        default=NOT_APPLICABLE,
    )

    tb_tx_given = models.ManyToManyField(
        TbTreatments,
        verbose_name="If YES, which treatment?",
        blank=True,
    )

    tb_tx_given_other = edc_models.OtherCharField()

    tb_tx_reason_no = models.CharField(
        verbose_name="If NO, give reason",
        max_length=30,
        choices=NEGATIVE_TX_CHOICES,
        default=NOT_APPLICABLE,
    )

    tb_tx_reason_no_other = edc_models.OtherCharField()

    on_steroids = models.CharField(
        verbose_name="Were steroids administered to the participant?",
        max_length=15,
        choices=YES_NO,
    )

    steroids_date = models.DateField(
        verbose_name="If YES, give date",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    steroids_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If YES, is this date estimated?",
        default=NOT_APPLICABLE,
    )

    steroids_given = models.CharField(
        verbose_name="If YES, which steroids?",
        max_length=35,
        choices=STEROID_CHOICES,
        default=NOT_APPLICABLE,
    )

    steroids_given_other = edc_models.OtherCharField()

    steroids_course = models.IntegerField(
        verbose_name="Length of steroid course?",
        validators=[MinValueValidator(0)],
        help_text="in days",
        null=True,
        blank=True,
    )

    # other treatment
    on_co_trimoxazole = models.CharField(
        verbose_name="Has the participant been prescribed co-trimoxazole?",
        max_length=15,
        choices=YES_NO,
        help_text="Select YES if currently on co-trimoxazole, or prescribed today.",
    )

    co_trimoxazole_date = models.DateField(
        verbose_name="If YES, give date",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    co_trimoxazole_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If YES, is this date estimated?",
        default=NOT_APPLICABLE,
    )

    co_trimoxazole_reason_no = models.CharField(
        verbose_name="If NO, give reason",
        max_length=30,
        choices=NEGATIVE_TX_CHOICES,
        default=NOT_APPLICABLE,
    )

    co_trimoxazole_reason_no_other = edc_models.OtherCharField()

    on_antibiotics = models.CharField(
        verbose_name="Has the participant been prescribed antibiotics?",
        max_length=15,
        choices=YES_NO,
    )

    antibiotics_date = models.DateField(
        verbose_name="If YES, give date",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    antibiotics_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If YES, is this date estimated?",
        default=NOT_APPLICABLE,
    )

    antibiotics_given = models.ManyToManyField(
        Antibiotics,
        verbose_name="If YES, which antibiotics?",
        blank=True,
    )

    antibiotics_given_other = edc_models.OtherCharField()

    on_other_drugs = models.CharField(
        verbose_name="Has the participant been prescribed any other drugs/interventions?",
        max_length=15,
        choices=YES_NO,
    )

    other_drugs_date = models.DateField(
        verbose_name="If YES, give date",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    other_drugs_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If YES, is this date estimated?",
        default=NOT_APPLICABLE,
    )

    other_drugs_given = models.ManyToManyField(
        Drugs,
        verbose_name="If YES, which drugs/interventions?",
        blank=True,
    )

    other_drugs_given_other = edc_models.OtherCharField()

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Participant Treatment"
        verbose_name_plural = "Participant Treatment"
