from django_db_views.db_view import DBView
from edc_qareports.model_mixins import (
    QaReportModelMixin,
    qa_reports_permissions,
)

from ...model_mixins import BaseBaselineVlModelMixin
from .view_definition import get_view_definition


class BaselineVlMissingQuantifier(BaseBaselineVlModelMixin, QaReportModelMixin, DBView):
    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "effect_reports_baselinevlmissingquantifierview"
        verbose_name = "Redmine #658.2 - Baseline Viral Load (Missing VL Quantifier)"
        verbose_name_plural = "Redmine #658.2 - Baseline Viral Loads (Missing VL Quantifier)"
        default_permissions = qa_reports_permissions
