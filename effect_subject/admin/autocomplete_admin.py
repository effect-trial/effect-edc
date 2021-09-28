from django.contrib import admin
from edc_list_data.admin import ListModelAdminMixin

from effect_lists.models import ArvRegimens

from ..admin_site import effect_subject_admin


@admin.register(ArvRegimens, site=effect_subject_admin)
class ArvRegimensAdmin(ListModelAdminMixin, admin.ModelAdmin):
    """Registered again for the autocomplete field"""

    pass
