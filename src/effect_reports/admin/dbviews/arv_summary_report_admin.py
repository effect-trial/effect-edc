from clinicedc_constants import NO, YES
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html
from edc_model_admin.dashboard import ModelAdminDashboardMixin
from edc_model_admin.mixins import TemplatesModelAdminMixin
from edc_qareports.modeladmin_mixins import QaReportModelAdminMixin
from edc_sites.admin import SiteModelAdminMixin

from effect_prn.models import ArvSummary

from ...admin_site import effect_reports_admin
from ...models import ArvSummaryReport


class CompletedListFilter(SimpleListFilter):
    title = "Completed"
    parameter_name = "completed"

    def lookups(self, request, model_admin):  # noqa: ARG002
        return (
            (YES, "Yes"),
            (NO, "No"),
        )

    def queryset(self, request, queryset):  # noqa: ARG002
        self.value()
        if self.value() == YES:
            subqs = ArvSummary.objects.all().values("subject_identifier")
            return queryset.filter(Q(subject_identifier__in=subqs))
        if self.value() == NO:
            subqs = ArvSummary.objects.all().values("subject_identifier")
            return queryset.filter(~Q(subject_identifier__in=subqs))
        return queryset


@admin.register(ArvSummaryReport, site=effect_reports_admin)
class ArvSummaryReportAdmin(
    QaReportModelAdminMixin,
    SiteModelAdminMixin,
    ModelAdminDashboardMixin,
    TemplatesModelAdminMixin,
    admin.ModelAdmin,
):
    include_note_column: bool = False

    ordering = ("subject_identifier",)

    list_display = ("subject_identifier", "arv_summary_link", "dashboard", "created")

    list_filter = (CompletedListFilter, "site")

    search_fields = ("subject_identifier",)

    @admin.display(description="Add/Edit", ordering="subject_identifier")
    def arv_summary_link(self, obj=None):
        try:
            arv_summary_obj = ArvSummary.objects.get(subject_identifier=obj.subject_identifier)
        except ObjectDoesNotExist:
            url = reverse("effect_prn_admin:effect_prn_arvsummary_add")
            label = "Add ARV Summary"
        else:
            url = reverse(
                "effect_prn_admin:effect_prn_arvsummary_change", args=(arv_summary_obj.id,)
            )
            label = "Edit ARV Summary"
        next_querystring = "effect_reports_admin:effect_reports_arvsummaryreport_changelist"
        return format_html(
            '<a href="{}?next={}&subject_identifier={}">{}</a>',
            url,
            next_querystring,
            obj.subject_identifier,
            label,
        )
