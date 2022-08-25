from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from effect_lists.models import Dx

from ..constants import IF_ADMITTED_COMPLETE_REPORTS, IF_YES_COMPLETE_AE
from ..model_mixins import CrfModelMixin


class Diagnoses(CrfModelMixin, edc_models.BaseUuidModel):

    # Diagnoses CRF (p3)
    # TODO: Move gi_side_effects into SiSx
    gi_side_effects = models.CharField(
        verbose_name="Has the participant experienced any gastrointestinal side effects?",
        max_length=15,
        # TODO: If yes, prompt for SAE form (where appropriate???)
        choices=YES_NO,
        help_text="If YES, complete SAE report where appropriate",
    )

    # TODO: Move gi_side_effects_other into SiSx
    gi_side_effects_details = models.TextField(
        verbose_name="If YES, please give details",
        null=True,
        blank=True,
    )

    # any_significant_new_diagnoses = models.CharField(
    #     # TODO: determine and display date of last visit
    #     verbose_name="Other significant new diagnoses since last visit?",
    #     max_length=15,
    #     choices=YES_NO,
    # )

    has_diagnoses = models.CharField(
        verbose_name="Are there any new significant diagnoses to report since last visit?",
        choices=YES_NO,
        max_length=15,
    )

    # TODO: ???If yes, date of diagnosis?
    # TODO: Request to handle one date per diagnosis

    # Significant Diagnoses CRF (p3)
    diagnoses = models.ManyToManyField(
        Dx, verbose_name="Please select all diagnoses that are relevant"
    )

    diagnoses_other = edc_models.OtherCharField()

    reportable_as_ae = models.CharField(
        verbose_name="Are any of these diagnoses Grade 3 or above?",
        max_length=15,
        # TODO: If yes, prompt for SAE
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=IF_YES_COMPLETE_AE,
    )

    patient_admitted = models.CharField(
        verbose_name="Has the participant been admitted due to any of these diagnoses?",
        max_length=15,
        # TODO: If yes, prompt for SAE form
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=IF_ADMITTED_COMPLETE_REPORTS,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Significant Diagnoses"
        verbose_name_plural = "Significant Diagnoses"
