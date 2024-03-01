from django.contrib.sites.managers import CurrentSiteManager
from edc_consent.managers import ConsentManager
from edc_model.models import HistoricalRecords

from .managers import SubjectConsentManager
from .subject_consent import SubjectConsent


class SubjectConsentV1(SubjectConsent):

    on_site = CurrentSiteManager()

    objects = SubjectConsentManager()

    consent = ConsentManager()

    history = HistoricalRecords()

    class Meta:
        proxy = True
        verbose_name = "Consent Version 1"
        verbose_name_plural = "Consent Version 1"
