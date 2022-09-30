from django.db import models
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN_NA_MISSED
from edc_constants.constants import NO, NOT_APPLICABLE
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_model import models as edc_models
from edc_offstudy.model_mixins import OffstudyNonCrfModelMixin
from edc_reference.model_mixins import ReferenceModelMixin
from edc_sites.models import SiteModelMixin
from edc_visit_tracking.choices import ASSESSMENT_TYPES
from edc_visit_tracking.managers import VisitCurrentSiteManager
from edc_visit_tracking.managers import VisitModelManager as BaseVisitModelManager
from edc_visit_tracking.model_mixins import VisitModelMixin

from ..choices import (
    ASSESSMENT_WHO_CHOICES,
    VISIT_INFO_SOURCE2,
    VISIT_REASON,
    VISIT_UNSCHEDULED_REASON,
)
from ..constants import IF_ADMITTED_COMPLETE_REPORTS


class VisitModelManager(BaseVisitModelManager):
    def create_missed_extras(self) -> dict:
        return dict(assessment_type=NOT_APPLICABLE, assessment_who=NOT_APPLICABLE)


class SubjectVisit(
    SiteModelMixin,
    VisitModelMixin,
    ReferenceModelMixin,
    CreatesMetadataModelMixin,
    RequiresConsentFieldsModelMixin,
    OffstudyNonCrfModelMixin,
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

    assessment_type = models.CharField(
        verbose_name="Was this a telephone or an in person visit?",
        max_length=15,
        choices=ASSESSMENT_TYPES,
    )

    assessment_type_other = edc_models.OtherCharField()

    assessment_who = models.CharField(
        verbose_name="Who did you speak to?",
        max_length=15,
        choices=ASSESSMENT_WHO_CHOICES,
    )

    assessment_who_other = edc_models.OtherCharField()

    # override default
    info_source = models.CharField(
        verbose_name="What is the MAIN source of this information?",
        max_length=25,
        choices=VISIT_INFO_SOURCE2,
    )

    hospitalized = models.CharField(
        verbose_name="Has the participant been hospitalized since the last assessment?",
        max_length=15,
        choices=YES_NO_UNKNOWN_NA_MISSED,
        # TODO: If yes, trigger AE Initial
        help_text=IF_ADMITTED_COMPLETE_REPORTS,
        default=NOT_APPLICABLE,
    )

    on_site = VisitCurrentSiteManager()

    objects = VisitModelManager()

    history = edc_models.HistoricalRecords()

    class Meta(VisitModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        pass
