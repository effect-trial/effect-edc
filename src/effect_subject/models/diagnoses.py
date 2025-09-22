from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from effect_lists.models import Dx

from ..model_mixins import CrfModelMixin, ReportingFieldsModelMixin


class Diagnoses(ReportingFieldsModelMixin, CrfModelMixin, edc_models.BaseUuidModel):
    # Diagnoses CRF (p3)
    gi_side_effects = models.CharField(
        verbose_name="Has the participant experienced any gastrointestinal side effects?",
        max_length=15,
        # TODO: If yes, prompt for SAE form (where appropriate???)
        choices=YES_NO,
        help_text="If YES, complete SAE report where appropriate",
    )

    gi_side_effects_details = models.TextField(
        verbose_name="If YES, please give details",
        blank=True,
        default="",
    )

    has_diagnoses = models.CharField(
        verbose_name="Are there any new significant diagnoses to report since last visit?",
        choices=YES_NO,
        max_length=15,
    )

    # Significant Diagnoses CRF (p3)
    diagnoses = models.ManyToManyField(
        Dx,
        verbose_name="Please select all diagnoses that are relevant",
    )

    diagnoses_other = models.TextField(
        verbose_name="If other, please specify ...",
        max_length=150,
        blank=True,
        default="",
    )

    # TODO: If not baseline, AND reportable_as_ae OR patient_admitted YES, prompt for SAE

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Significant Diagnoses"
        verbose_name_plural = "Significant Diagnoses"
