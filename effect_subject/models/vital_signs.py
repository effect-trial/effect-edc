from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_model import models as edc_models
from edc_vitals.models import WeightField

from effect_subject.choices import MEASURED_EST_CHOICES
from effect_subject.fields.temperature import TemperatureField

from ..model_mixins import CrfModelMixin


class VitalSigns(CrfModelMixin, edc_models.BaseUuidModel):

    weight = WeightField(null=True)

    weight_measured_or_est = models.CharField(
        verbose_name="Is the weight estimated or measured?",
        max_length=25,
        choices=MEASURED_EST_CHOICES,
    )

    heart_rate = models.IntegerField(
        verbose_name="Heart rate:",
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        help_text="BPM",
    )

    respiratory_rate = models.IntegerField(
        verbose_name="Respiratory rate:",
        validators=[MinValueValidator(6), MaxValueValidator(50)],
        help_text="breaths/min",
        null=True,
    )

    temperature = TemperatureField()

    reportable_as_ae = models.CharField(
        verbose_name="Are any of the above reportable as Grade 3 or above?",
        max_length=15,
        # TODO: If yes, prompt for SAE
        choices=YES_NO_NA,
    )

    patient_admitted = models.CharField(
        verbose_name="Has the patient been admitted due to any of the above?",
        max_length=15,
        # TODO: If yes, prompt for SAE form
        choices=YES_NO,
        help_text="If yes, complete SAE report",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Vital Signs"
        verbose_name_plural = "Vital Signs"
