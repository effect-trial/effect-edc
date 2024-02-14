from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future, datetime_not_future
from edc_offstudy.constants import END_OF_STUDY_ACTION
from edc_protocol.validators import date_not_before_study_start
from edc_sites.model_mixins import SiteModelMixin
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from effect_lists.models import LateExclusionCriteria, OffstudyReasons


class EndOfStudy(SiteModelMixin, OffScheduleModelMixin, ActionModelMixin, BaseUuidModel):
    action_name = END_OF_STUDY_ACTION

    offschedule_datetime = models.DateTimeField(
        verbose_name="Date participant was terminated from the study",
        validators=[datetime_not_future],
        blank=False,
        null=True,
    )

    offschedule_reason = models.ForeignKey(
        OffstudyReasons,
        verbose_name="Reason participant was terminated from the study",
        on_delete=models.PROTECT,
        null=True,
    )

    other_offschedule_reason = models.TextField(
        verbose_name="If OTHER, please specify reason ...",
        max_length=500,
        blank=True,
        null=True,
    )

    death_date = models.DateField(
        verbose_name="If died, what was the date of death?",
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True,
    )

    ltfu_date = models.DateField(
        verbose_name="If lost to follow-up, on what date?",
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True,
    )

    consent_withdrawal_reason = models.TextField(
        verbose_name="If participant withdrew consent, please specify reason ...",
        max_length=500,
        blank=True,
        null=True,
    )

    late_exclusion_reasons = models.ManyToManyField(
        LateExclusionCriteria,
        verbose_name="If fulfilled late exclusion criteria, please specify which ...",
        blank=True,
        help_text="Select all that apply.",
    )

    transferred_consent = models.CharField(
        verbose_name=(
            "If transferred, has the participant provided consent to be "
            "followed-up for 6 month end-point?"
        ),
        choices=YES_NO_NA,
        max_length=15,
        default=NOT_APPLICABLE,
    )

    invalid_enrol_reason = models.TextField(
        verbose_name="If participant was included in error, please provide narrative ...",
        max_length=500,
        blank=True,
        null=True,
    )

    comment = models.TextField(
        verbose_name="Please provide further details if possible",
        max_length=500,
        blank=True,
        null=True,
    )

    class Meta(OffScheduleModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "End of Study"
        verbose_name_plural = "End of Study"
