from django.contrib import admin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import effect_ae_admin
from ..forms import AeSponsorReviewForm
from ..models import AeSponsorReview
from .modeladmin_mixins import AeReviewModelAdminMixin


@admin.register(AeSponsorReview, site=effect_ae_admin)
class AeSponsorReviewAdmin(AeReviewModelAdminMixin, SimpleHistoryAdmin):

    form = AeSponsorReviewForm
