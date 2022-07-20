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
            "Education",
            {
                "fields": (
                    "occupation",
                    "education_years",
                    "education_certificate",
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
                    "welfare",
                    "monthly_household_income",
                    "is_highest_earner",
                    "profession_highest_earner",
                ),
            },
        ),
        (
            "General expenditure",
            {
                "fields": (
                    "monthly_food",
                    "monthly_accommodation",
                    "yearly_large_items",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "higher_education": admin.VERTICAL,
        "is_highest_earner": admin.VERTICAL,
        "primary_school": admin.VERTICAL,
        "secondary_school": admin.VERTICAL,
        "welfare": admin.VERTICAL,
    }
