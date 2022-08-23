from django.contrib import admin
from edc_adverse_event.modeladmin_mixins import AeTmgModelAdminMixin
from edc_model_admin.history import SimpleHistoryAdmin

from ..admin_site import effect_ae_admin
from ..forms import AeTmgForm
from ..models import AeTmg


@admin.register(AeTmg, site=effect_ae_admin)
class AeTmgAdmin(AeTmgModelAdminMixin, SimpleHistoryAdmin):

    form = AeTmgForm
