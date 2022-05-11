from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models
from edc_vitals.model_mixins import SimpleBloodPressureModelMixin
from edc_vitals.models import WeightField

from ..choices import MEASURED_EST_CHOICES
from ..constants import (
    IF_ADMITTED_COMPLETE_REPORTS,
    IF_YES_COMPLETE_AE,
    VITAL_SIGNS_ACTION,
)
from ..fields.temperature import TemperatureField


class VitalSigns(
    SimpleBloodPressureModelMixin, CrfWithActionModelMixin, edc_models.BaseUuidModel
):

    action_name = VITAL_SIGNS_ACTION

    tracking_identifier_prefix = "VS"

    action_identifier = models.CharField(max_length=50, unique=True, null=True)

    tracking_identifier = models.CharField(max_length=30, unique=True, null=True)

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
        default=NOT_APPLICABLE,
        help_text=IF_YES_COMPLETE_AE,
    )

    patient_admitted = models.CharField(
        verbose_name="Has the patient been admitted due to any of the above?",
        max_length=15,
        # TODO: If yes, prompt for SAE form
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=IF_ADMITTED_COMPLETE_REPORTS,
    )

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Vital Signs"
        verbose_name_plural = "Vital Signs"
