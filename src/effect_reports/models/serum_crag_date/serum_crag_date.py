from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions


class SerumCragDate(QaReportModelMixin, models.Model):
    """Model class for a QA Report that lists subjects who have
    consented and need the Serum Crag Date from screening to be
    confirmed. The report works together with model
    SerumCragDateNote.
    """

    # Current serum_crag_date in screening model.
    # This date is to be confirmed on the SerumCragDateNote model.
    serum_crag_date = models.DateField(null=True)

    # helper information
    screening_identifier = models.CharField(
        verbose_name="Screening ID",
        max_length=50,
        null=True,
    )

    # helper information
    eligibility_date = models.DateField(null=True)

    # helper information
    serum_crag_value = models.CharField(
        verbose_name="CrAg",
        max_length=50,
        null=True,
    )

    objects = models.Manager()

    class Meta(QaReportModelMixin.Meta):
        verbose_name = "Redmine #488.1 - Serum Crag Date (Confirmation)"
        verbose_name_plural = "Redmine #488.1 - Serum Crag Dates (Confirmation)"
        default_permissions = qa_reports_permissions
