from django.contrib import admin
from edc_consent.modeladmin_mixins import ModelAdminConsentMixin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_consent_admin
from ..forms import SubjectConsentForm
from ..models import SubjectConsentV1
from .modeladmin_mixins import EffectSubjectConsentAdminMixin


@admin.register(SubjectConsentV1, site=effect_consent_admin)
class SubjectConsentV1Admin(
    EffectSubjectConsentAdminMixin,
    SiteModelAdminMixin,
    ModelAdminConsentMixin,
    ModelAdminSubjectDashboardMixin,
    SimpleHistoryAdmin,
):
    form = SubjectConsentForm

    readonly_fields = []

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)
        fieldsets = list(fieldsets)
        for index, fieldset in enumerate(fieldsets):
            if fieldset[0] == "Substudy, Specimens and Data Sharing":
                fieldsets.remove(fieldset)
                break
        return tuple(fieldsets)
