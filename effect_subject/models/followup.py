from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import DEAD
from edc_crf.crf_with_action_model_mixin import CrfWithActionModelMixin
from edc_model import models as edc_models

from ..choices import ASSESSMENT_TYPES, INFO_SOURCES, PATIENT_STATUSES
from ..constants import ALIVE_UNWELL, FOLLOWUP_ACTION, IF_YES_COMPLETE_SAE, PATIENT


class Followup(CrfWithActionModelMixin, edc_models.BaseUuidModel):

    # TODO: Schedule for d1 and d14

    action_name = FOLLOWUP_ACTION

    tracking_identifier_prefix = "FU"

    action_identifier = models.CharField(max_length=50, unique=True, null=True)

    tracking_identifier = models.CharField(max_length=30, unique=True, null=True)

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
        help_text=(
            f"If subject '{dict(PATIENT_STATUSES)[ALIVE_UNWELL]}, "
            "consider unscheduled visit, or AE report. "
            f"If subject '{dict(PATIENT_STATUSES)[DEAD]}', submit death report"
        ),
    )

    hospitalized = models.CharField(
        verbose_name="Has the patient been hospitalized since the last assessment?",
        max_length=15,
        choices=YES_NO,
        help_text=IF_YES_COMPLETE_SAE,
    )

    adherence_counselling = models.CharField(
        verbose_name="Was adherence counselling given?",
        max_length=15,
        choices=YES_NO_NA,
    )

    class Meta(CrfWithActionModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Follow-up"
        verbose_name_plural = "Follow-up"
