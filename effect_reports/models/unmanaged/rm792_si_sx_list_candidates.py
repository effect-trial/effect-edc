from django.contrib.sites.models import Site
from django.db import models
from django.db.models import PROTECT


class Rm792SiSxListCandidates(models.Model):
    report_model = models.CharField(max_length=50)

    site = models.ForeignKey(Site, on_delete=PROTECT)

    created = models.DateTimeField()

    current_sx_other = models.TextField()

    class Meta:
        managed = False
        db_table = "rm792_si_sx_list_candidates"
        verbose_name = "Redmine #792.3: Signs and Symptoms: Possible list candidates"
        verbose_name_plural = "Redmine #792.3: Signs and Symptoms: Possible list candidates"
