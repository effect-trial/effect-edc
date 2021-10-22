from django.db import models
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NO, NOT_APPLICABLE
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_model import models as edc_models
from edc_reference.model_mixins import ReferenceModelMixin
from edc_sites.models import CurrentSiteManager as BaseCurrentSiteManager
from edc_sites.models import SiteModelMixin
from edc_visit_tracking.managers import VisitModelManager
from edc_visit_tracking.model_mixins import VisitModelMixin

from ..choices import (
    ASSESSMENT_METHODS,
    INFO_SOURCE,
    INFO_SOURCE_WHO_CHOICES,
    PATIENT_STATUSES,
    VISIT_REASON,
    VISIT_UNSCHEDULED_REASON,
)


class CurrentSiteManager(VisitModelManager, BaseCurrentSiteManager):
    pass


class SubjectVisit(
    VisitModelMixin,
    ReferenceModelMixin,
    CreatesMetadataModelMixin,
    SiteModelMixin,
    RequiresConsentFieldsModelMixin,
    edc_models.BaseUuidModel,
):

    """A model completed by the user that captures the covering
    information for the data collected for this timepoint/appointment,
    e.g.report_datetime.
    """

    # override default
    reason = models.CharField(
        verbose_name="What is the reason for this visit report?",
        max_length=25,
        choices=VISIT_REASON,
        help_text="If 'missed', fill in the separate missed visit report",
    )

    # override default
    reason_unscheduled = models.CharField(
        verbose_name="If 'unscheduled', provide reason for the unscheduled visit",
        max_length=25,
        choices=VISIT_UNSCHEDULED_REASON,
        default=NOT_APPLICABLE,
    )

    unschedule_self_referral = models.CharField(
        verbose_name="If 'unschedule', is this a self-referral?",
        max_length=25,
        choices=YES_NO,
        default=NO,
    )

    unschedule_detail = models.TextField(
        verbose_name="If 'unschedule', please provide further details, if any",
        null=True,
        blank=True,
    )

    # override default
    info_source = models.CharField(
        verbose_name="What is the main source of this information?",
        max_length=25,
        choices=INFO_SOURCE,
    )

    # TODO: ???Reconcile with info_source? ???Redundant?
    info_source_who = models.CharField(
        verbose_name="Who did you speak to?",
        max_length=15,
        choices=INFO_SOURCE_WHO_CHOICES,
    )

    assessment_method = models.CharField(
        verbose_name="Was this a telephone follow up or an in person visit?",
        max_length=15,
        choices=ASSESSMENT_METHODS,
    )

    patient_status = models.CharField(
        verbose_name="Patient status?",
        max_length=15,
        # TODO: If dead, prompt for death & SAE form
        choices=PATIENT_STATUSES,
    )

    date_of_death_known = models.CharField(
        verbose_name="Is the date of death known?",
        max_length=15,
        choices=YES_NO_NA,
    )

    date_of_death = models.DateField(
        verbose_name="Date of death",
        validators=[edc_models.date_not_future],
        null=True,
    )

    date_of_death_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If date of death provided, is this date estimated?"
    )
    on_site = CurrentSiteManager()

    objects = VisitModelManager()

    history = edc_models.HistoricalRecords()

    class Meta(VisitModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        pass
