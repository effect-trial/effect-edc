from django.db import models
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions

from .model_mixins import BaseBaselineVlModelMixin


class BaselineVlDiscrepancy(
    BaseBaselineVlModelMixin,
    UniqueSubjectIdentifierFieldMixin,
    QaReportModelMixin,
    BaseUuidModel,
):
    """A data management table to list baseline VL results with
    discrepancies around the responses to `has_viral_load_result` and
    the other related VL questions.

    See class BaselineVlDiscrepancyDf. For example, to populate:
        df_cls = BaselineVlDiscrepancyDf()
        df_cls.to_model(model="effect_reports.baselinevldiscrepancy")

    Populated in the modeladmin.get_queryset
    """

    report_model = models.CharField(
        max_length=50,
        default="effect_reports.baselinevldiscrepancy",
    )

    class Meta(QaReportModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Redmine #658.3 - Baseline Viral Load (Discrepancy)"
        verbose_name_plural = "Redmine #658.3 - Baseline Viral Loads (Discrepancies)"
        default_permissions = qa_reports_permissions
