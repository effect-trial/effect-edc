from django.core.validators import MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_model import models as edc_models

from effect_lists.models import Antibiotics, TbTreatments
from effect_subject.choices import CM_TX_CHOICES, STEROID_CHOICES

from ..model_mixins import CrfModelMixin


class StudyTreatment(CrfModelMixin, edc_models.BaseUuidModel):

    # Patient Treatment CRF (p4)
    lp_completed = models.CharField(
        verbose_name="LP completed?",
        max_length=15,
        # TODO: If yes, prompt for lab results
        choices=YES_NO,
        help_text="If yes, complete laboratory results",
    )

    cm_confirmed = models.CharField(
        verbose_name="Cryptococcal meningitis confirmed?",
        max_length=15,
        choices=YES_NO_NA,
    )

    cm_tx_administered = models.CharField(
        verbose_name="Cryptococcal meningitis treatment administered?",
        max_length=15,
        choices=YES_NO_NA,
    )

    cm_tx_given = models.CharField(
        verbose_name="Cryptococcal meningitis treatment given?",
        max_length=15,
        choices=CM_TX_CHOICES,
    )

    cm_tx_given_other = edc_models.OtherCharField(
        verbose_name="If other CM treatment given, please specify ..."
    )

    tb_tx_given = models.ManyToManyField(
        TbTreatments,
        verbose_name="TB treatment given?",
        blank=True,
    )

    tb_tx_given_other = edc_models.OtherCharField(
        verbose_name="If other TB treatment given, please specify ..."
    )

    steroids_administered = models.CharField(
        verbose_name="Steroids administered?",
        max_length=15,
        choices=YES_NO,
    )

    which_steroids = models.CharField(
        verbose_name="If yes, which steroids where administered?",
        max_length=35,
        choices=STEROID_CHOICES,
    )

    which_steroids_other = edc_models.OtherCharField()

    steroids_course_duration = models.IntegerField(
        verbose_name="Length of steroid course?",
        validators=[MinValueValidator(0)],
        help_text="in days",
        null=True,
        blank=True,
    )

    # other treatment
    co_trimoxazole = models.CharField(
        verbose_name="Co-Trimoxazole given?",
        max_length=15,
        choices=YES_NO,
    )

    # TODO: ???d1 only?
    antibiotics = models.ManyToManyField(
        Antibiotics,
        verbose_name="Antibiotics?",
        blank=True,
    )

    antibiotics_other = edc_models.OtherCharField(
        verbose_name="If other antibiotics, please specify ..."
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Study Treatment"
        verbose_name_plural = "Study Treatment"
