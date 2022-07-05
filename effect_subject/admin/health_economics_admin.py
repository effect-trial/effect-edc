from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ..admin_site import effect_subject_admin
from ..models import HealthEconomicsBaselineTermination
from .modeladmin import CrfModelAdmin


@admin.register(HealthEconomicsBaselineTermination, site=effect_subject_admin)
class HealthEconomicsBaselineTerminationAdmin(CrfModelAdmin):

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Education",
            {
                "fields": (
                    "occupation",
                    "education_years",
                    "highest_education_certificate",
                    "primary_school",
                    "primary_school_years",
                    "secondary_school",
                    "secondary_school_years",
                    "higher_education",
                    "higher_education_years",
                ),
            },
        ),
        (
            "Income",
            {
                "fields": (
                    "welfare_social_service_support",
                    "monthly_household_income",
                    "highest_income_person",
                    "highest_income_person_profession",
                ),
            },
        ),
        (
            "General expenditure",
            {
                "fields": (
                    "monthly_household_food_spent",
                    "monthly_household_rent_spent",
                    "yearly_household_large_item_spent",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "occupation",
        "education_years",
        "highest_education_certificate",
        "primary_school",
        "primary_school_years",
        "secondary_school",
        "secondary_school_years",
        "higher_education",
        "higher_education_years",
    )

    list_filter = (
        "report_datetime",
        "primary_school",
        "secondary_school",
        "higher_education",
    )

    search_fields = ("report_datetime",)

    radio_fields = {
        "higher_education": admin.VERTICAL,
        "highest_income_person": admin.VERTICAL,
        "primary_school": admin.VERTICAL,
        "secondary_school": admin.VERTICAL,
        "welfare_social_service_support": admin.VERTICAL,
    }
