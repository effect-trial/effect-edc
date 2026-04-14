from __future__ import annotations

from django.contrib import admin

from ...admin_site import effect_reports_admin
from ...modeladmin_mixins.baseline_vl_modeladmin_mixin import BaselineVlModelAdminMixin
from ...models import BaselineVlMissingQuantifier


@admin.register(BaselineVlMissingQuantifier, site=effect_reports_admin)
class BaselineVlMissingQuantifierAdmin(BaselineVlModelAdminMixin, admin.ModelAdmin):
    report_model = "effect_reports.baselinevlmissingquantifier"
