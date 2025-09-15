from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import HealthEconomicsEventForm
from ..models import HealthEconomicsEvent
from .modeladmin import CrfModelAdmin


@admin.register(HealthEconomicsEvent, site=effect_subject_admin)
class HealthEconomicsEventAdmin(CrfModelAdmin):
    form = HealthEconomicsEventForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Earlier health care expenses",
            {
                "fields": (
                    "buy_meds",
                    "arv_spend",
                    "meds_other_spend",
                    "arv_payee",
                    "meds_other_payee",
                    "health_activities",
                    "health_activities_detail",
                    "health_activities_spend",
                    "health_activities_payee",
                    "healthcare_month",
                ),
            },
        ),
        (
            "Loss of productivity and earnings",
            {
                "fields": (
                    "routine_activities_disrupted_days",
                    "routine_activities",
                    "routine_activities_other",
                    "time_off_days",
                    "travel_time",
                    "hospital_time",
                    "lost_income",
                    "lost_income_amount",
                ),
            },
        ),
        (
            "Family loss of productivity and earnings",
            {
                "fields": (
                    "childcare",
                    "childcare_source",
                    "childcare_source_other",
                    "childcare_source_time_off_days",
                ),
            },
        ),
        (
            "Current visit transport, health care and other expenses",
            {
                "fields": (
                    "transport",
                    "transport_other",
                    "transport_spend",
                    "food_spend",
                    "buy_meds_today",
                    "arv_spend_today",
                    "meds_other_spend_today",
                    "arv_payee_today",
                    "meds_other_payee_today",
                    "health_activities_today",
                    "health_activities_detail_today",
                    "health_activities_spend_today",
                ),
            },
        ),
        (
            "Hospital stay",
            {
                "fields": (
                    "admitted",
                    "admitted_admin",
                    "admitted_admin_spend",
                    "admitted_investigations",
                    "admitted_investigations_spend",
                    "admitted_food_spend",
                    "admitted_other_spend",
                    "admitted_time_off",
                    "admitted_carers",
                    "admitted_visitors",
                    "admitted_kith_kin_time_off",
                    "admitted_kith_kin_month",
                ),
            },
        ),
        (
            "Health care financing",
            {
                "fields": (
                    "sell_to_pay",
                    "borrow_to_pay",
                    "health_insurance",
                    "health_insurance_month",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    filter_horizontal = ("transport",)

    radio_fields = {  # noqa: RUF012
        "admitted": admin.VERTICAL,
        "admitted_admin": admin.VERTICAL,
        "admitted_investigations": admin.VERTICAL,
        "admitted_kith_kin_time_off": admin.VERTICAL,
        "admitted_time_off": admin.VERTICAL,
        "arv_payee": admin.VERTICAL,
        "arv_payee_today": admin.VERTICAL,
        "borrow_to_pay": admin.VERTICAL,
        "buy_meds": admin.VERTICAL,
        "buy_meds_today": admin.VERTICAL,
        "childcare": admin.VERTICAL,
        "childcare_source": admin.VERTICAL,
        "health_activities": admin.VERTICAL,
        "health_activities_payee": admin.VERTICAL,
        "health_activities_today": admin.VERTICAL,
        "health_insurance": admin.VERTICAL,
        "lost_income": admin.VERTICAL,
        "meds_other_payee": admin.VERTICAL,
        "meds_other_payee_today": admin.VERTICAL,
        "routine_activities": admin.VERTICAL,
        "sell_to_pay": admin.VERTICAL,
    }
