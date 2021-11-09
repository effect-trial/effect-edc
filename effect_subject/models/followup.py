from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from ..choices import ASSESSMENT_TYPES, INFO_SOURCES, PATIENT_STATUSES
from ..constants import PATIENT
from ..model_mixins import CrfModelMixin


class Followup(CrfModelMixin, edc_models.BaseUuidModel):

    # TODO: Schedule for d1 and d14

    assessment_type = models.CharField(
        verbose_name="Was this a telephone follow up or an in person visit?",
        max_length=15,
        choices=ASSESSMENT_TYPES,
    )

    info_source = models.CharField(
        verbose_name="If by telephone, who did you speak to?",
        max_length=15,
        choices=INFO_SOURCES,
        default=PATIENT,
    )

    info_source_other = edc_models.OtherCharField()

    survival_status = models.CharField(
        verbose_name="What is the patient status?",
        max_length=15,
        # TODO: Validate against visit survival status
        # TODO: If dead, trigger SAE -> death form -> off study
        choices=PATIENT_STATUSES,
    )

    hospitalized = models.CharField(
        verbose_name="Has the patient been hospitalized since the last assessment?",
        max_length=15,
        # TODO: If yes, trigger SAE
        choices=YES_NO,
    )

    adherence_counselling = models.CharField(
        verbose_name="Was adherence counselling given?",
        max_length=15,
        choices=YES_NO,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Clinical Assessment"
        verbose_name_plural = "Clinical Assessment"
