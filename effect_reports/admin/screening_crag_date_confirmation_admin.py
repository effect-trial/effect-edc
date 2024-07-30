from django.contrib import admin
from django.db.models import Case, DurationField, ExpressionWrapper, F, When
from django.db.models.functions import TruncDate
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin.dashboard import (
    ModelAdminDashboardMixin,
    ModelAdminSubjectDashboardMixin,
)
from edc_model_admin.history import SimpleHistoryAdmin
from edc_sites.admin import SiteModelAdminMixin

from ..admin_site import effect_reports_admin
from ..forms import ScreeningCragDateConfirmationForm
from ..models import ScreeningCragDateConfirmation


@admin.register(ScreeningCragDateConfirmation, site=effect_reports_admin)
class ScreeningCragDateConfirmationAdmin(
    SiteModelAdminMixin,
    ModelAdminSubjectDashboardMixin,
    ModelAdminDashboardMixin,  # ???
    SimpleHistoryAdmin,
):
    form = ScreeningCragDateConfirmationForm
    ordering = ("subject_identifier",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "report_datetime",
                    "screening_identifier",
                    "subject_identifier",
                    "initials",
                )
            },
        ),
        # (
        #     "xxx",
        #     {
        #         "fields": (
        #             "screening_identifier",
        #             "subject_identifier",
        #             "initials",
        #         )
        #     },
        # ),
        (
            "Screening Serum CrAg Date Confirmation",
            {
                "fields": (
                    "confirmed_dob",
                    "confirmed_gender",
                    "confirmed_serum_crag_date",
                )
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "confirmed_gender": admin.VERTICAL,
    }

    list_display = [
        "subject_identifier",
        # "dashboard",
        "initials",
        "screening_identifier",
        # "report_datetime",
        # "confirmed_dob",
        # "confirmed_gender",
        "confirmed_serum_crag_date_",
        "days_from_eligibility_date",
        "days_from_serum_crag_date",
        # "created",
        # "modified",
        # "user_created",
        # "user_modified",
    ]

    search_fields = [
        "screening_identifier",
        "subject_identifier",
    ]

    @admin.display(description="Confirmed Serum CrAg", ordering="confirmed_serum_crag_date")
    def confirmed_serum_crag_date_(self, obj=None):
        return obj.confirmed_serum_crag_date

    @admin.display(description="Eligibility Diff", ordering="eligibility_date_delta")
    def days_from_eligibility_date(self, obj=None):
        if obj.eligibility_date_delta:
            days = obj.eligibility_date_delta.days
            return f"{'+' if days > 0 else ''}{days}d"

    @admin.display(description="Serum CrAg Diff", ordering="serum_crag_date_delta")
    def days_from_serum_crag_date(self, obj=None):
        if obj.serum_crag_date_delta:
            days = obj.serum_crag_date_delta.days
            return f"{'+' if days > 0 else ''}{days}d"

    def get_list_filter(self, request) -> tuple[str, ...]:
        list_filter = super().get_list_filter(request)
        custom_fields = ("confirmed_serum_crag_date",)
        return custom_fields + tuple(f for f in list_filter if f not in custom_fields)

    def get_readonly_fields(self, request, obj=None) -> tuple:
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        return readonly_fields + (
            "subject_identifier",
            "initials",
        )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                eligibility_date_delta=Case(
                    When(
                        confirmed_serum_crag_date__isnull=False,
                        then=ExpressionWrapper(
                            F("confirmed_serum_crag_date")
                            - TruncDate(F("eligibility_datetime")),
                            output_field=DurationField(),
                        ),
                    ),
                    default=None,
                ),
                serum_crag_date_delta=Case(
                    When(
                        confirmed_serum_crag_date__isnull=False,
                        then=ExpressionWrapper(
                            F("confirmed_serum_crag_date") - F("serum_crag_date"),
                            output_field=DurationField(),
                        ),
                    ),
                    default=None,
                ),
            )
        )
