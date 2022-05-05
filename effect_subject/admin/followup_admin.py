from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_action_item import (
    ModelAdminActionItemMixin,
    action_fields,
    action_fieldset_tuple,
)
from edc_model_admin import SimpleHistoryAdmin

from ..admin_site import effect_subject_admin
from ..forms import FollowupForm
from ..models import Followup
from .modeladmin import CrfModelAdminMixin


@admin.register(Followup, site=effect_subject_admin)
class FollowupAdmin(
    CrfModelAdminMixin,
    ModelAdminActionItemMixin,
    SimpleHistoryAdmin,
):

    form = FollowupForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        action_fieldset_tuple,
        audit_fieldset_tuple,
    )

    readonly_fields = action_fields

    radio_fields = {}
