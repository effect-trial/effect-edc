from django.db import models
from django_pandas.managers import DataFrameManager
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_qareports.model_mixins import QaReportModelMixin


class BaseBaselineVlModelMixin(
    UniqueSubjectIdentifierFieldMixin,
    QaReportModelMixin,
    BaseUuidModel,
):
    """A modelmixin for VL data management tables with details of each
    participant's baseline viral load.
    """

    crf_id = models.UUIDField(null=True)
    visit_code = models.CharField(max_length=25, null=True)
    visit_code_sequence = models.IntegerField(default=0, null=True)

    has_viral_load_result = models.CharField(max_length=5, null=True)
    viral_load_result = models.IntegerField(null=True)
    viral_load_quantifier = models.CharField(max_length=20, null=True)
    viral_load_date = models.DateField(null=True)
    viral_load_date_estimated = models.CharField(max_length=50, null=True)

    user_created = models.CharField(max_length=50, null=True)
    user_modified = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)

    objects = DataFrameManager()

    class Meta(BaseUuidModel.Meta):
        abstract = True
