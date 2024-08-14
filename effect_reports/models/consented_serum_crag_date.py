from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin


class ConsentedSerumCragDate(QaReportModelMixin, models.Model):

    screening_identifier = models.CharField(
        verbose_name="Screening ID",
        max_length=50,
        null=True,
    )

    serum_crag_date = models.DateField(null=True)

    eligibility_date = models.DateField(null=True)

    serum_crag_value = models.CharField(
        verbose_name="CrAg",
        max_length=50,
        null=True,
    )

    objects = models.Manager()

    class Meta(QaReportModelMixin.Meta):
        verbose_name = "Redmine #488.1 Consented Serum Crag Date"
        verbose_name_plural = "Redmine #488.1 Consented Serum Crag Dates"
