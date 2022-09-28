from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import AeFollowupModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import effect_ae_admin
from ..forms import AeFollowupForm
from ..models import AeFollowup


@admin.register(AeFollowup, site=effect_ae_admin)
class AeFollowupAdmin(AeFollowupModelAdminMixin, SimpleHistoryAdmin):

    form = AeFollowupForm
