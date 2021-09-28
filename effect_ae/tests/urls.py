from django.contrib import admin
from django.urls.conf import include, path

from effect_ae.admin_site import meta_ae_admin

urlpatterns = [
    path("ae/", include("effect_ae.urls")),
    path("admin/", meta_ae_admin.urls),
    path("admin/", admin.site.urls),
]
