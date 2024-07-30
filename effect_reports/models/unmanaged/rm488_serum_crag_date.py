from django.db import models
from django_crypto_fields.fields import EncryptedCharField
from edc_qareports.models import QaReportModelMixin


class Rm488SerumCragDate(QaReportModelMixin, models.Model):
    # Rm488SerumCragDateConsented
    screening_identifier = models.CharField(max_length=50)
    initials = EncryptedCharField()
    age_in_years = models.IntegerField()
    gender = models.CharField(max_length=10)

    eligibility_date = models.DateField()
    serum_crag_date = models.DateField()
    days_difference = models.IntegerField()
    # confirmed_serum_crag_date = models.DateField()

    user_created = models.CharField(max_length=25)
    user_modified = models.CharField(max_length=25)
    # created = models.DateTimeField()
    # modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "rm488_serum_crag_date"
        verbose_name = "Redmine #488.2: Serum Grag Date (orig WIP)"
        verbose_name_plural = "Redmine #488.2: xxx (orig WIP)"
