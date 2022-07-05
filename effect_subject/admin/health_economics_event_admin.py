from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..forms import HealthEconomicsForm
from ..models import HealthEconomics
from .modeladmin import CrfModelAdmin


@admin.register(HealthEconomics, site=effect_subject_admin)
class HealthEconomicsAdmin(CrfModelAdmin):

    form = HealthEconomicsForm

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Earlier health care expenses",
            {
                "fields": (
                    "buy_refill_drug",
                    "amount_spent_antiretroviral_drugs_past",
                    "amount_spent_other_drugs_past",
                    "payment_method_antiretroviral_drugs_past",
                    "payment_method_other_drugs_past",
                    "spent_money_other_health_activities_past",
                    "other_health_activities_past",
                    "amount_spent_other_health_activities_past",
                    "payment_method_other_health_activities_past",
                    "num_day_activities_disrupted",
                    "amount_spent_healthcare_last_month",
                ),
            },
        ),
        (
            "Loss of productivity and earnings",
            {
                "fields": (
                    "activities_not_come_clinic",
                    "activities_not_come_clinic_other",
                    "time_taken_off_work",
                    "time_taken_get_here",
                    "time_spent_clinic",
                    "loss_earnings",
                    "loss_earnings_amount",
                ),
            },
        ),
        (
            "Family loss of productivity and earnings",
            {
                "fields": (
                    "someone_looking_children",
                    "someone_looking_children_activities",
                    "someone_looking_children_activities_other",
                    "someone_looking_children_time_spent",
                ),
            },
        ),
        (
            "Current visit transport, health care and other expenses",
            {
                "fields": (
                    "transport_used",
                    "transport_used_other",
                    "transport_used_amount",
                    "amount_spent_food",
                    "get_drugs_visit_today",
                    "amount_spent_antiretroviral_drugs_today",
                    "amount_spent_other_drugs_today",
                    "payment_method_antiretroviral_drugs_today",
                    "payment_method_other_drugs_today",
                    "spent_money_other_health_activities_today",
                    "other_health_activities_today",
                    "amount_spent_other_health_activities_today",
                ),
            },
        ),
        (
            "Hospital stay",
            {
                "fields": (
                    "administrative_charges",
                    "administrative_charges_amount",
                    "admitted_day_pay_for_tests",
                    "admitted_day_amount_pay_for_tests",
                    "admitted_day_amount_spent_food",
                    "admitted_amount_spent_other_items",
                    "admitted_time_off_work",
                    "admitted_num_people_stay_with_you",
                    "admitted_num_people_visit_you",
                    "admitted_people_time_off_work",
                    "admitted_people_time_off_work_amount_monthly",
                ),
            },
        ),
        (
            "Health care financing",
            {
                "fields": (
                    "sale_anything_pay_visit_today",
                    "loan_pay_visit_treatment",
                    "private_healthcare",
                    "private_healthcare_amount_monthly",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "buy_refill_drug",
        "amount_spent_antiretroviral_drugs_past",
        "amount_spent_other_drugs_past",
        "spent_money_other_health_activities_past",
        "other_health_activities_past",
    )

    list_filter = ("report_datetime",)

    search_fields = ("report_datetime",)

    filter_horizontal = [
        "transport_used",
    ]

    radio_fields = {
        "activities_not_come_clinic": admin.VERTICAL,
        "administrative_charges": admin.VERTICAL,
        "admitted_day_pay_for_tests": admin.VERTICAL,
        "admitted_people_time_off_work": admin.VERTICAL,
        "admitted_time_off_work": admin.VERTICAL,
        "buy_refill_drug": admin.VERTICAL,
        "get_drugs_visit_today": admin.VERTICAL,
        "loan_pay_visit_treatment": admin.VERTICAL,
        "loss_earnings": admin.VERTICAL,
        "payment_method_antiretroviral_drugs_past": admin.VERTICAL,
        "payment_method_antiretroviral_drugs_today": admin.VERTICAL,
        "payment_method_other_drugs_past": admin.VERTICAL,
        "payment_method_other_drugs_today": admin.VERTICAL,
        "payment_method_other_health_activities_past": admin.VERTICAL,
        "private_healthcare": admin.VERTICAL,
        "sale_anything_pay_visit_today": admin.VERTICAL,
        "someone_looking_children": admin.VERTICAL,
        "someone_looking_children_activities": admin.VERTICAL,
        "spent_money_other_health_activities_past": admin.VERTICAL,
        "spent_money_other_health_activities_today": admin.VERTICAL,
    }
