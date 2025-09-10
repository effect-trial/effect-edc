from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "effect_export"

urlpatterns = [
    path("", RedirectView.as_view(url="/effect_export/admin/"), name="home_url"),
]
