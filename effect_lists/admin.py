from django.contrib import admin
from edc_list_data.admin import ListModelAdminMixin

from .admin_site import effect_lists_admin
from .models import (
    ArvRegimens,
    NonAdherenceReasons,
    OffstudyReasons,
    SubjectVisitMissedReasons,
)


@admin.register(SubjectVisitMissedReasons, site=effect_lists_admin)
class SubjectVisitMissedReasonsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ArvRegimens, site=effect_lists_admin)
class ArvRegimensAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(OffstudyReasons, site=effect_lists_admin)
class OffstudyReasonsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(NonAdherenceReasons, site=effect_lists_admin)
class NonAdherenceReasonsAdmin(ListModelAdminMixin, admin.ModelAdmin):
    pass
