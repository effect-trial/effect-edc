from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from effect_subject.choices import ECOG_SCORES, MODIFIED_RANKIN_SCORE_CHOICES

from ..model_mixins import CrfModelMixin


class MentalStatus(CrfModelMixin, edc_models.BaseUuidModel):

    recent_seizure = models.CharField(
        verbose_name="Recent seizure (<72 hours)?",
        max_length=15,
        choices=YES_NO,
    )

    behaviour_change = models.CharField(
        verbose_name="Behaviour change?",
        max_length=15,
        choices=YES_NO,
    )

    confusion = models.CharField(
        verbose_name="Confusion?",
        max_length=15,
        choices=YES_NO,
    )

    modified_rankin_score = models.CharField(
        verbose_name="Modified Rankin Score?",
        max_length=15,
        choices=MODIFIED_RANKIN_SCORE_CHOICES,
    )

    ecog_score = models.CharField(
        verbose_name="ECOG score?",
        max_length=15,
        choices=ECOG_SCORES,
    )

    # See: https://www.ncbi.nlm.nih.gov/books/NBK513298/#article-22258.s3
    glasgow_coma_score = models.IntegerField(
        verbose_name="Glasgow Coma Score?",
        validators=[MinValueValidator(3), MaxValueValidator(15)],
        help_text="/15",
    )

    reportable_as_ae = models.CharField(
        verbose_name="Are any of these symptoms Grade 3 or above?",
        max_length=15,
        # TODO: If yes, prompt for SAE
        choices=YES_NO,
    )

    patient_admitted = models.CharField(
        verbose_name="Has the patient been admitted due to these symptoms?",
        max_length=15,
        # TODO: If yes, prompt for SAE form
        choices=YES_NO,
        help_text="If yes, complete SAE report",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Mental Status"
        verbose_name_plural = "Mental Status"
