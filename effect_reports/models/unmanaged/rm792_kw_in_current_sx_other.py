from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class Rm792KwInCurrentSxOther(QaReportModelMixin, models.Model):

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField(default=0)

    current_sx_other = models.TextField()

    user_created = models.CharField(max_length=25)

    user_modified = models.CharField(max_length=25)

    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "rm792_kw_in_current_sx_other"
        verbose_name = "Redmine #792.1: Signs and Symptoms: Keyword in other sx"
        verbose_name_plural = "Redmine #792.1: Signs and Symptoms: Keyword in other sx"
        default_permissions = qa_reports_permissions
