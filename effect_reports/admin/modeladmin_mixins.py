from django.apps import apps as django_apps
from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin


class BaselineVlModelAdminMixin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
):
    report_model: str = None
    site_list_display_insert_pos: int = 2
    qa_report_list_display_insert_pos = 8
    ordering = ["site", "subject_identifier"]

    list_display = [
        "dashboard",
        "update_crf",
        "subject",
        "has_viral_load_result",
        "viral_load_result",
        "viral_load_quantifier",
        "viral_load_date",
        "viral_load_date_estimated",
        "user_created",
        "user_modified",
        "created",
        "modified",
    ]

    list_filter = (
        "has_viral_load_result",
        "viral_load_result",
        "viral_load_quantifier",
        "viral_load_date",
        "viral_load_date_estimated",
        "site_id",
        "user_created",
        "user_modified",
        "created",
        "modified",
    )

    search_fields = [
        "subject_identifier",
        "viral_load_result",
    ]

    @admin.display(description="Update")
    def update_crf(self, obj=None):
        crf_model_cls = django_apps.get_model("effect_subject.arvhistory")
        crf_model_cls.objects.get(id=obj.crf_id)
        url = reverse(
            f"{self.crf_admin_site_name(crf_model_cls)}:"
            f"{crf_model_cls._meta.label_lower.replace('.', '_')}_change",
            args=(obj.crf_id,),
        )
        url = (
            f"{url}?next={self.admin_site.name}:"
            f"{self.model._meta.label_lower.replace('.', '_')}_changelist"
        )
        title = _(f"Change {crf_model_cls._meta.verbose_name}")
        label = _("Change CRF")
        crf_button = render_to_string(
            "edc_qareports/columns/change_button.html",
            context=dict(title=title, url=url, label=label),
        )
        return crf_button

    @admin.display(description="subject", ordering="subject_identifier")
    def subject(self, obj=None):
        return obj.subject_identifier

    @staticmethod
    def crf_admin_site_name(crf_model_cls) -> str:
        """Returns the name of the admin site CRFs are registered
        by assuming admin site name follows the edc naming convention.

        For example: 'meta_subject_admin' or 'effect_subject_admin'
        """
        return f"{crf_model_cls._meta.label_lower.split('.')[0]}_admin"
