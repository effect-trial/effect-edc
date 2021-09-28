from django.contrib import admin
from django.urls.conf import include, path

from effect_prn.admin_site import effect_prn_admin

urlpatterns = [
    path("effect_prn/", include("effect_prn.urls")),
    path("admin/", effect_prn_admin.urls),
    path("admin/", admin.site.urls),
]
