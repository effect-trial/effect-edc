from django.apps import apps as django_apps
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from edc_consent.field_mixins import (
    CitizenFieldsMixin,
    IdentityFieldsMixin,
    PersonalFieldsMixin,
    ReviewFieldsMixin,
    SampleCollectionFieldsMixin,
    VulnerabilityFieldsMixin,
)
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_identifier.subject_identifier import SubjectIdentifier as BaseSubjectIdentifier
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_search.model_mixins import SearchSlugManager
from edc_sites.models import SiteModelMixin

from .model_mixins import SearchSlugModelMixin


class SubjectIdentifier(BaseSubjectIdentifier):
    template = "{protocol_number}-{site_id}-{sequence}"
    padding = 4


class SubjectConsentManager(SearchSlugManager, models.Manager):
    def get_by_natural_key(self, subject_identifier, version):
        return self.get(subject_identifier=subject_identifier, version=version)


# TODO: may want to allow for a witness if required. Not just linked to literacy.
# TODO: Languages: Xhosa, Afrikaans, Sesotho, Setswana, Zulu
# TODO: Add Kyla's checklist on literacy, etc


class SubjectConsent(
    ConsentModelMixin,
    SiteModelMixin,
    UpdatesOrCreatesRegistrationModelMixin,
    NonUniqueSubjectIdentifierModelMixin,
    IdentityFieldsMixin,
    ReviewFieldsMixin,
    PersonalFieldsMixin,
    SampleCollectionFieldsMixin,
    CitizenFieldsMixin,
    VulnerabilityFieldsMixin,
    SearchSlugModelMixin,
    BaseUuidModel,
):

    """A model completed by the user that captures the ICF."""

    subject_identifier_cls = SubjectIdentifier

    subject_screening_model = "effect_screening.subjectscreening"

    screening_identifier = models.CharField(
        verbose_name="Screening identifier", max_length=50, unique=True
    )

    screening_datetime = models.DateTimeField(
        verbose_name="Screening datetime", null=True, editable=False
    )

    completed_by_next_of_kin = models.CharField(
        max_length=10, default=NO, choices=YES_NO, editable=False
    )

    is_able = models.CharField(
        verbose_name="Is the participant able to provide consent?",
        max_length=3,
        choices=YES_NO,
        default=YES,
        help_text=(
            "If 'No' provide witness's name on this "
            "form and signature on the paper document."
        ),
    )

    on_site = CurrentSiteManager()

    objects = SubjectConsentManager()

    consent = ConsentManager()

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.subject_identifier} V{self.version}"

    def save(self, *args, **kwargs):
        subject_screening = self.get_subject_screening()
        self.screening_datetime = subject_screening.report_datetime
        self.subject_type = "subject"
        self.citizen = NOT_APPLICABLE
        super().save(*args, **kwargs)

    def natural_key(self):
        return self.subject_identifier, self.version

    def get_subject_screening(self):
        """Returns the subject screening model instance.

        Instance must exist since SubjectScreening is completed
        before consent.
        """
        model_cls = django_apps.get_model(self.subject_screening_model)
        return model_cls.objects.get(screening_identifier=self.screening_identifier)

    @property
    def registration_unique_field(self):
        """Required for UpdatesOrCreatesRegistrationModelMixin."""
        return "subject_identifier"

    class Meta(ConsentModelMixin.Meta, BaseUuidModel.Meta):
        unique_together = (
            ("subject_identifier", "version"),
            ("subject_identifier", "screening_identifier"),
            ("first_name", "dob", "initials", "version"),
        )
