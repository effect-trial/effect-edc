from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_vitals.model_mixins import SimpleBloodPressureModelMixin
from edc_vitals.models import WeightField

from ..choices import MEASURED_EST_CHOICES
from ..fields.temperature import TemperatureField


class VitalsFieldsModelMixin(SimpleBloodPressureModelMixin, models.Model):

    weight = WeightField(null=True)

    weight_measured_or_est = models.CharField(
        verbose_name="Is the weight estimated or measured?",
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

    class Meta:
        abstract = True
