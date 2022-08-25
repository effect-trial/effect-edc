from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from ..choices import ECOG_SCORES, MODIFIED_RANKIN_SCORE_CHOICES
from ..constants import IF_ADMITTED_COMPLETE_REPORTS, IF_YES_COMPLETE_AE
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

    require_help = models.CharField(
        verbose_name="Does the participant require help from anybody for everyday activities?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="Answer only at scheduled Week 10 and Month 6 visits",
    )

    any_other_problems = models.CharField(
        verbose_name="Has the illness left the participant with any other problems?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="Answer only at scheduled Week 10 and Month 6 visits",
    )

    modified_rankin_score = models.CharField(
        verbose_name="Modified Rankin Score",
        max_length=15,
        choices=MODIFIED_RANKIN_SCORE_CHOICES,
    )

    ecog_score = models.CharField(
        verbose_name="ECOG score",
        max_length=15,
        choices=ECOG_SCORES,
    )

    # See: https://www.ncbi.nlm.nih.gov/books/NBK513298/#article-22258.s3
    glasgow_coma_score = models.IntegerField(
        verbose_name="Glasgow Coma Score",
        validators=[MinValueValidator(3), MaxValueValidator(15)],
        help_text="/15",
    )

    reportable_as_ae = models.CharField(
        verbose_name="Are any of these symptoms Grade 3 or above?",
        max_length=15,
        # TODO: If yes, prompt for SAE
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=IF_YES_COMPLETE_AE,
    )

    patient_admitted = models.CharField(
        verbose_name="Has the participant been admitted due to these symptoms?",
        max_length=15,
        # TODO: If yes, prompt for SAE form
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=IF_ADMITTED_COMPLETE_REPORTS,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Mental Status"
        verbose_name_plural = "Mental Status"
