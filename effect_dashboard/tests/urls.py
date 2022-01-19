from django.contrib import admin
from django.urls.conf import include, path
from django.views.generic.base import RedirectView
from edc_action_item.admin_site import edc_action_item_admin
from edc_appointment.admin_site import edc_appointment_admin
from edc_consent.admin_site import edc_consent_admin
from edc_dashboard.views import AdministrationView
from edc_locator.admin_site import edc_locator_admin
from edc_reference.admin_site import edc_reference_admin

from effect_ae.admin_site import effect_ae_admin
from effect_consent.admin_site import effect_consent_admin
from effect_prn.admin_site import effect_prn_admin
from effect_screening.admin_site import effect_screening_admin
from effect_subject.admin_site import effect_subject_admin

from .admin import effect_test_admin

urlpatterns = [
    path("accounts/", include("edc_auth.urls")),
    path("admin/", include("edc_auth.urls")),
    path("admin/", edc_appointment_admin.urls),
    path("admin/", edc_consent_admin.urls),
    path("admin/", effect_test_admin.urls),
    path("admin/", effect_ae_admin.urls),
    path("admin/", effect_prn_admin.urls),
    path("admin/", edc_reference_admin.urls),
    path("admin/", edc_locator_admin.urls),
    path("admin/", effect_consent_admin.urls),
    path("admin/", effect_subject_admin.urls),
    path("admin/", effect_screening_admin.urls),
    path("admin/", edc_action_item_admin.urls),
    path("admin/", admin.site.urls),
    path("administration/", AdministrationView.as_view(), name="administration_url"),
    path("effect_ae/", include("effect_ae.urls")),
    path("effect_prn/", include("effect_prn.urls")),
    path("effect_screening/", include("effect_screening.urls")),
    path("effect_consent/", include("effect_consent.urls")),
    path("effect_subject/", include("effect_subject.urls")),
    path("edc_action_item/", include("edc_action_item.urls")),
    path("edc_adverse_event/", include("edc_adverse_event.urls")),
    path("edc_appointment/", include("edc_appointment.urls")),
    path("edc_auth/", include("edc_auth.urls")),
    path("edc_consent/", include("edc_consent.urls")),
    path("edc_dashboard/", include("edc_dashboard.urls")),
    path("edc_data_manager/", include("edc_data_manager.urls")),
    path("edc_device/", include("edc_device.urls")),
    path("edc_lab/", include("edc_lab.urls")),
    path("edc_export/", include("edc_export.urls")),
    path("edc_lab_dashboard/", include("edc_lab_dashboard.urls")),
    path("edc_locator/", include("edc_locator.urls")),
    path("edc_pharmacy_dashboard/", include("edc_pharmacy_dashboard.urls")),
    path("edc_protocol/", include("edc_protocol.urls")),
    path("edc_reference/", include("edc_reference.urls")),
    path("edc_subject_dashboard/", include("edc_subject_dashboard.urls")),
    path("edc_visit_schedule/", include("edc_visit_schedule.urls")),
    path("subject/", include("effect_dashboard.urls")),
    path("", RedirectView.as_view(url="admin/"), name="home_url"),
]
