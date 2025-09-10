from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "effect_ae"

urlpatterns = [
    path("", RedirectView.as_view(url="/effect_ae/admin/"), name="home_url"),
]
