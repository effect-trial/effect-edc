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
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_identifier.subject_identifier import SubjectIdentifier as BaseSubjectIdentifier
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_sites.model_mixins import SiteModelMixin

from .managers import SubjectConsentManager
from .model_mixins import SearchSlugModelMixin
from .special_consent_fields_model_mixin import SpecialConsentFieldsModelMixin


class SubjectIdentifier(BaseSubjectIdentifier):
    template = "{protocol_number}-{site_id}-{sequence}"
    padding = 4


# TODO: may want to allow for a witness if required. Not just linked to literacy.
# TODO: Languages: Xhosa, Afrikaans, Sesotho, Setswana, Zulu
# TODO: Add Kyla's checklist on literacy, etc


class SubjectConsent(
    SpecialConsentFieldsModelMixin,
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
        model_cls = django_apps.get_model(self.consent_definition.screening_model)
        return model_cls.objects.get(screening_identifier=self.screening_identifier)

    @property
    def registration_unique_field(self):
        """Required for UpdatesOrCreatesRegistrationModelMixin."""
        return "subject_identifier"

    class Meta(ConsentModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Consent"
        verbose_name_plural = "Consents"
        # unique_together = (
        #     # ("subject_identifier", "version"),
        #     ("subject_identifier", "screening_identifier", "version"),
        #     # ("first_name", "dob", "initials", "version"),
        # )
