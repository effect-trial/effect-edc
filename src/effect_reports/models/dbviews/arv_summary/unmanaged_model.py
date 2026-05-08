from django_db_views.db_view import DBView
from edc_qareports.model_mixins import (
    QaReportModelMixin,
    qa_reports_permissions,
)

from .view_definition import get_view_definition


class ArvSummaryReport(QaReportModelMixin, DBView):
    view_definition = get_view_definition()

    class Meta:
        managed = False
        db_table = "effect_reports_arvsummaryview"
        verbose_name = "Arv summary to complete"
        verbose_name_plural = "ARV Summarys to complete"
        default_permissions = qa_reports_permissions
