from django.contrib.admin import AdminSite as DjangoAdminSite
from edc_locator.models import SubjectLocator

from effect_consent.models import SubjectConsent
from effect_screening.models import SubjectScreening
from effect_subject.models import SubjectRequisition, SubjectVisit


class AdminSite(DjangoAdminSite):
    site_title = "Ambition Subject"
    site_header = "Ambition Subject"
    index_title = "Ambition Subject"
    site_url = "/administration/"


effect_test_admin = AdminSite(name="effect_test_admin")

effect_test_admin.register(SubjectScreening)
effect_test_admin.register(SubjectConsent)
effect_test_admin.register(SubjectLocator)
effect_test_admin.register(SubjectVisit)
effect_test_admin.register(SubjectRequisition)
