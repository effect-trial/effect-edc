from django.db import models
from edc_model.models import BaseUuidModel
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
        verbose_name = "Redmine #658.1 - Baseline Viral Load (All)"
        verbose_name_plural = "Redmine #658.1 - Baseline Viral Loads (All)"
        default_permissions = qa_reports_permissions


class BaselineVlMissingQuantifier(BaseBaselineVlModelMixin):
    """A data management table to list baseline VL results where a VL
    result has been entered, but no corresponding
    `viral_load_quantifier` has been set.

    See class BaselineVlMissingQuantifierDf. For example, to populate:
        df_cls = BaselineVlMissingQuantifierDf()
        df_cls.to_model(model="effect_reports.baselinevlmissingquantifier")

    Populated in the modeladmin.get_queryset
    """

    report_model = models.CharField(
        max_length=50, default="effect_reports.baselinevlmissingquantifier"
    )

    class Meta(QaReportModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Redmine #658.2 - Baseline Viral Load (Missing VL Quantifier)"
        verbose_name_plural = "Redmine #658.2 - Baseline Viral Loads (Missing VL Quantifier)"
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

    class Meta(QaReportModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Redmine #658.3 - Baseline Viral Load (Discrepancy)"
        verbose_name_plural = "Redmine #658.3 - Baseline Viral Loads (Discrepancies)"
        default_permissions = qa_reports_permissions
