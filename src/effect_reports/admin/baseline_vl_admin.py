from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin

from ..admin_site import effect_reports_admin
from ..dataframes import (
    BaselineVlAllDf,
    BaselineVlDiscrepancyDf,
    BaselineVlMissingQuantifierDf,
)
from ..modeladmin_mixins.baseline_vl_modeladmin_mixin import BaselineVlModelAdminMixin
from ..models import BaselineVlAll, BaselineVlMissingQuantifier

if TYPE_CHECKING:
    from django.db.models import QuerySet


@admin.register(BaselineVlAll, site=effect_reports_admin)
class BaselineVlAllAdmin(BaselineVlModelAdminMixin, admin.ModelAdmin):
    report_model = "effect_reports.baselinevlall"

    def get_queryset(self, request) -> QuerySet:
        df_cls = BaselineVlAllDf()
        df_cls.to_model(model=self.report_model)
        return super().get_queryset(request)


@admin.register(BaselineVlMissingQuantifier, site=effect_reports_admin)
class BaselineVlMissingQuantifierAdmin(BaselineVlModelAdminMixin, admin.ModelAdmin):
    report_model = "effect_reports.baselinevlmissingquantifier"

    def get_queryset(self, request) -> QuerySet:
        df_cls = BaselineVlMissingQuantifierDf()
        df_cls.to_model(model=self.report_model)
        return super().get_queryset(request)


# @admin.register(BaselineVlDiscrepancy, site=effect_reports_admin)
class BaselineVlDiscrepancyAdmin(BaselineVlModelAdminMixin, admin.ModelAdmin):
    report_model = "effect_reports.baselinevldiscrepancy"

    def get_queryset(self, request) -> QuerySet:
        df_cls = BaselineVlDiscrepancyDf()
        df_cls.to_model(model=self.report_model)
        return super().get_queryset(request)
