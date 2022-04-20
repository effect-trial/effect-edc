from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_identifier.model_mixins import TrackingModelMixin
from edc_model.models import BaseUuidModel, date_not_future, datetime_not_future
from edc_offstudy.constants import END_OF_STUDY_ACTION
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from effect_lists.models import OffstudyReasons
from effect_prn.choices import (
    DIAGNOSIS,
    FLUCONAZOLE_DOSE_14DAYS,
    FLUCONAZOLE_DOSE_CONSOLIDATION,
    MEDICINES,
    STUDY_TERMINATION_REASONS,
)


class EndOfStudy(
    OffScheduleModelMixin, ActionModelMixin, TrackingModelMixin, BaseUuidModel
):

    action_name = END_OF_STUDY_ACTION

    tracking_identifier_prefix = "ST"

    offschedule_datetime = models.DateTimeField(
        verbose_name="Date patient was terminated from the study",
        validators=[datetime_not_future],
        help_text="This can include date of: lost to follow up; withdrawal, Death, Calendar month 6",
        blank=False,
        null=True,
    )

    lastfollowup_datetime = models.DateTimeField(
        verbose_name="Date of last research follow-up",
        validators=[datetime_not_future],
        blank=False,
        null=True,
    )

    admitted_for_cm = models.CharField(
        verbose_name="Was the patient admitted at any time for cryptococcal meningitis?",
        choices=YES_NO,
        max_length=45,
        blank=False,
        null=True,
    )

    no_admissions = models.IntegerField(
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

    other_offschedule_reason = models.TextField(
        verbose_name="If OTHER, please specify", max_length=500, blank=True, null=True
    )

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
            "If transferred, has the patient provided consent to be followed-up for 6 month end-point?"
        ),
        choices=YES_NO_NA,
        max_length=15,
        default=NOT_APPLICABLE,
    )

    medication_study_termination = models.CharField(
        verbose_name="Medicines on Study Termination day",
        choices=MEDICINES,
        max_length=45,
    )

    other_medication_study_termination = models.TextField(
        verbose_name="If OTHER, please specify", max_length=500, blank=True, null=True
    )

    diagnoses_since_enrolment = models.CharField(
        verbose_name="Other significant diagnoses since enrolment",
        choices=YES_NO,
        max_length=15,
    )

    diagnoses_datetime = models.DateField(
        verbose_name="If Yes, date of diagnosis",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    diagnoses = models.CharField(
        verbose_name="If Yes, diagnosis",
        choices=DIAGNOSIS,
        max_length=45,
    )

    other_diagnoses = models.TextField(
        verbose_name="If Other, please specify", max_length=500, blank=True, null=True
    )

    missed_doses_5fc = models.CharField(
        verbose_name="Is there any missed doses in first 14 days: 5FC",
        choices=YES_NO,
        max_length=15,
    )

    no_missed_doses_5fc = models.IntegerField(
        verbose_name="Number of doses missed in first 14 days: 5FC",
        blank=True,
        null=True,
    )

    missed_doses_flu = models.CharField(
        verbose_name="Is there any missed doses in first 14 days: FLU",
        choices=YES_NO,
        max_length=15,
    )

    no_missed_doses_flu = models.IntegerField(
        verbose_name="Number of doses missed in first 14 days: FLU",
        blank=True,
        null=True,
    )

    fluconazole_dose_14days = models.CharField(
        verbose_name="Fluconazole dose taken during first 14days of study",
        choices=FLUCONAZOLE_DOSE_14DAYS,
        max_length=15,
    )

    other_fluconazole_dose_14days = models.CharField(
        verbose_name="If Other, please specify",
        max_length=45,
        blank=True,
        null=True,
    )

    reasons = models.TextField(
        verbose_name="Reasons",
        max_length=500,
        blank=True,
        null=True,
    )

    missed_doses_consolidation_flu = models.CharField(
        verbose_name="Is there any missed doses during consolidation/maintenance phase: FLU",
        choices=YES_NO,
        max_length=15,
    )

    no_missed_doses_consolidation_flu = models.IntegerField(
        verbose_name="Total number of doses missed during consolidation/maintenance phase: FLU",
        blank=True,
        null=True,
    )

    fluconazole_consolidation_phase = models.CharField(
        verbose_name="Fluconazole dose taken during consolidation/maintenance phase",
        choices=FLUCONAZOLE_DOSE_CONSOLIDATION,
        max_length=15,
    )

    other_fluconazole_consolidation_phase = models.CharField(
        verbose_name="If Other, please specify",
        max_length=45,
        blank=True,
        null=True,
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
