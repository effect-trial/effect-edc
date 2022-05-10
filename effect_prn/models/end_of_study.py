from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_identifier.model_mixins import TrackingModelMixin
from edc_model.models import (
    BaseUuidModel,
    OtherCharField,
    date_not_future,
    datetime_not_future,
)
from edc_offstudy.constants import END_OF_STUDY_ACTION
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from effect_prn.choices import STUDY_TERMINATION_REASONS


class EndOfStudy(OffScheduleModelMixin, ActionModelMixin, TrackingModelMixin, BaseUuidModel):
    action_name = END_OF_STUDY_ACTION

    tracking_identifier_prefix = "ST"

    offschedule_datetime = models.DateTimeField(
        verbose_name="Date patient was terminated from the study",
        validators=[datetime_not_future],
        blank=False,
        null=True,
    )

    lastfollowup_datetime = models.DateField(
        verbose_name="Date of last research follow-up",
        validators=[date_not_future],
        blank=False,
        null=True,
    )

    cm_admitted = models.CharField(
        verbose_name="Was the patient admitted at any time for cryptococcal meningitis?",
        choices=YES_NO,
        max_length=45,
        blank=False,
        null=True,
    )

    cm_admitted_cnt = models.IntegerField(
        verbose_name="If yes, number of admissions for CM",
        blank=True,
        null=True,
    )

    offschedule_reason = models.CharField(
        verbose_name="Reason patient was terminated from the study",
        choices=STUDY_TERMINATION_REASONS,
        max_length=50,
        null=True,
    )

    offschedule_reason_other = OtherCharField()

    withdrawal_consent_reasons = models.TextField(
        verbose_name="If withdrawal Consent, please specify reasons",
        max_length=500,
        blank=True,
        null=True,
    )

    late_exclusion_reasons = models.TextField(
        verbose_name="If late exclusion for other reason, specify reason",
        max_length=500,
        blank=True,
        null=True,
    )

    transferred_consent = models.CharField(
        verbose_name=(
            "If transferred, has the patient provided consent to be "
            "followed-up for 6 month end-point?"
        ),
        choices=YES_NO_NA,
        max_length=15,
        default=NOT_APPLICABLE,
    )

    comment = models.TextField(
        verbose_name="Please provide further details if possible",
        max_length=500,
        blank=True,
        null=True,
    )

    class Meta(OffScheduleModelMixin.Meta):
        verbose_name = "End of Study"
        verbose_name_plural = "End of Study"
