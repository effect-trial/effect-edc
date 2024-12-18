from django.db import models
from edc_qareports.model_mixins import QaReportModelMixin, qa_reports_permissions

from .model_mixins import BaseBaselineVlModelMixin


class BaselineVlAll(BaseBaselineVlModelMixin):
    """A data management table to list ALL baseline VL results.

    See class BaselineVlAllDf. For example, to populate:
        df_cls = BaselineVlAllDf()
        df_cls.to_model(model="effect_reports.baselinevlall")

    Populated in the modeladmin.get_queryset
    """

    report_model = models.CharField(max_length=50, default="effect_reports.baselinevlall")

    class Meta(QaReportModelMixin.Meta):
        db_table = "effect_reports_baselinevlall"
        verbose_name = "Redmine #658.1 - Baseline Viral Load (All)"
        verbose_name_plural = "Redmine #658.1 - Baseline Viral Loads (All)"
        default_permissions = qa_reports_permissions


class BaselineVlDiscrepancy(BaseBaselineVlModelMixin):
    """A data management table to list baseline VL results with
    discrepancies around the responses to `has_viral_load_result` and
    the other related VL questions.

    See class BaselineVlDiscrepancyDf. For example, to populate:
        df_cls = BaselineVlDiscrepancyDf()
        df_cls.to_model(model="effect_reports.baselinevldiscrepancy")

    Populated in the modeladmin.get_queryset
    """

    report_model = models.CharField(
        max_length=50, default="effect_reports.baselinevldiscrepancy"
    )

    class Meta(QaReportModelMixin.Meta):
        db_table = "effect_reports_baselinevldiscrepancy"
        verbose_name = "Redmine #658.2 - Baseline Viral Load (Discrepancy)"
        verbose_name_plural = "Redmine #658.2 - Baseline Viral Loads (Discrepancies)"
        default_permissions = qa_reports_permissions
