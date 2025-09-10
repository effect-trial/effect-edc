from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class Rm792KwInCurrentSxGteG3Other(QaReportModelMixin, models.Model):

    visit_code = models.CharField(max_length=25)

    visit_code_sequence = models.IntegerField(default=0)

    crf_id = models.UUIDField(null=True)

    current_sx_gte_g3_other = models.TextField()

    user_created = models.CharField(max_length=25)

    user_modified = models.CharField(max_length=25)

    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "rm792_kw_in_current_sx_gte_g3_other"
        verbose_name = "Redmine #792.2 - Signs and Symptoms: Keyword in other G3 sx"
        verbose_name_plural = "Redmine #792.2 - Signs and Symptoms: Keyword in other G3 sx"
        default_permissions = qa_reports_permissions
