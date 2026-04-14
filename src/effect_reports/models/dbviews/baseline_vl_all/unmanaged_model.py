from django_db_views.db_view import DBView
from edc_qareports.model_mixins import (
    QaReportModelMixin,
    qa_reports_permissions,
)

from ...model_mixins import BaseBaselineVlModelMixin
from .view_definition import get_view_definition


class BaselineVlAll(BaseBaselineVlModelMixin, QaReportModelMixin, DBView):
    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "effect_reports_baselinevlallview"
        verbose_name = "Redmine #658.1 - Baseline Viral Load (All)"
        verbose_name_plural = "Redmine #658.1 - Baseline Viral Loads (All)"
        default_permissions = qa_reports_permissions
