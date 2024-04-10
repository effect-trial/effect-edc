from django.contrib import admin
from edc_consent.modeladmin_mixins import ModelAdminConsentMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_consent_admin
from ..forms import SubjectConsentForm
from ..models import SubjectConsent
from .modeladmin_mixins import EffectSubjectConsentAdminMixin


@admin.register(SubjectConsent, site=effect_consent_admin)
class SubjectConsentAdmin(
    EffectSubjectConsentAdminMixin,
    SiteModelAdminMixin,
    ModelAdminConsentMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentForm
