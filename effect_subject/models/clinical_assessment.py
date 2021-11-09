from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA, YES_NO_UNKNOWN
from edc_model import models as edc_models

from effect_lists.models import (
    Antibiotics,
    ArvRegimens,
    Drugs,
    FocalNeurologicDeficits,
    TbTreatments,
    XRayResults,
)

from ..choices import (
    ASSESSMENT_METHODS,
    CM_TX_CHOICES,
    ECOG_SCORES,
    MODIFIED_RANKIN_SCORE_CHOICES,
    PATIENT_STATUSES,
    SPOKE_TO_CHOICES,
    STEROID_CHOICES,
)
from ..model_mixins import CrfModelMixin


class ClinicalAssessment(CrfModelMixin, edc_models.BaseUuidModel):

    # TODO: Schedule for d1 and d14

    # Initial Clinical Assessment CRF (p1)
    who_speak_to = models.CharField(
        verbose_name="Who did you speak to?",
        max_length=15,
        choices=SPOKE_TO_CHOICES,
    )

    who_speak_to_other = edc_models.OtherCharField()

    assessment_method = models.CharField(
        verbose_name="Was this a telephone follow up or an in person visit?",
        max_length=15,
        choices=ASSESSMENT_METHODS,
    )

    patient_hospitalized = models.CharField(
        verbose_name="Has the patient been hospitalized",
        max_length=15,
        # TODO: If yes, trigger SAE
        choices=YES_NO_NA,
    )

    patient_status = models.CharField(
        verbose_name="Patient status?",
        max_length=15,
        # TODO: Validate against visit survival status
        # TODO: If dead, trigger SAE -> death form -> off study
        choices=PATIENT_STATUSES,
    )

    adherence_counselling = models.CharField(
        verbose_name="Was adherence counselling given?",
        max_length=15,
        choices=YES_NO_NA,
    )

    # Vital Signs CRF (p2)
    # vitals_fields_model_mixin configured for vitals
    # TODO: Move TemperatureField to core edc(-vitals)
    # TODO: ???Implement RespiratoryRateField and HeartRateField?

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Clinical Assessment"
        verbose_name_plural = "Clinical Assessment"
