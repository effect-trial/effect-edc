from django.urls.conf import path
from django.views.generic import RedirectView

app_name = "effect_subject"

urlpatterns = [
    path("", RedirectView.as_view(url="/effect_subject/admin/"), name="home_url"),
]
