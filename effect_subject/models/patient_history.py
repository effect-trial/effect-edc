from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from effect_lists.models import Medication

from ..choices import FLUCONAZOLE_DOSES
from ..model_mixins import CrfModelMixin


class PatientHistory(CrfModelMixin, edc_models.BaseUuidModel):

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

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Patient History"
        verbose_name_plural = "Patient History"
