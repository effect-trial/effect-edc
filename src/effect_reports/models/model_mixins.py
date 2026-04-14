from django.db import models
from django_pandas.managers import DataFrameManager


class BaseBaselineVlModelMixin(models.Model):
    """A modelmixin for VL data management tables with details of each
    participant's baseline viral load.
    """

    crf_id = models.UUIDField(null=True)

    visit_code_str = models.CharField(max_length=25, default="")

    has_viral_load_result = models.CharField(max_length=5, default="")
    viral_load_result = models.IntegerField(null=True)
    viral_load_quantifier = models.CharField(max_length=20, default="")
    viral_load_date = models.DateField(null=True)
    viral_load_date_estimated = models.CharField(max_length=50, default="")

    user_created = models.CharField(max_length=50, default="")
    user_modified = models.CharField(max_length=50, default="")
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    objects = DataFrameManager()

    class Meta:
        abstract = True
