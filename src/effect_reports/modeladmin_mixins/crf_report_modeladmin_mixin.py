from django.apps import apps as django_apps
from django.contrib import admin
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CrfReportModelAdminMixin:
    crf_model: str | None = None

    @admin.display(description="Update")
    def update_crf(self, obj=None):
        crf_model_cls = django_apps.get_model(self.crf_model)
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
        title = _("Change {verbose_name}").format(
            verbose_name=crf_model_cls._meta.verbose_name
        )
        label = _("Change CRF")
        return render_to_string(
            "edc_qareports/columns/change_button.html",
            context=dict(title=title, url=url, label=label),
        )

    @staticmethod
    def crf_admin_site_name(crf_model_cls) -> str:
        """Returns the name of the admin site CRFs are registered
        by assuming admin site name follows the edc naming convention.

        For example: 'meta_subject_admin' or 'effect_subject_admin'
        """
        return f"{crf_model_cls._meta.label_lower.split('.')[0]}_admin"
