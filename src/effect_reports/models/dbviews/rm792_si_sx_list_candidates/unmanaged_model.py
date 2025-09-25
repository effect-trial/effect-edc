from django.db import models
from django_db_views.db_view import DBView
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions

from .view_definition import get_view_definition


class Rm792SiSxListCandidates(QaReportModelMixin, DBView):
    view_definition = get_view_definition()

    current_sx_other = models.TextField()

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = "rm792_si_sx_list_candidates"
        verbose_name = "Redmine #792.3 - Signs and Symptoms: Possible list candidates"
        verbose_name_plural = "Redmine #792.3 - Signs and Symptoms: Possible list candidates"
        default_permissions = qa_reports_permissions
