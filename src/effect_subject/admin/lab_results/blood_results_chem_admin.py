from django.contrib import admin
from edc_action_item.fieldsets import action_fieldset_tuple
from edc_lab_results.admin import BloodResultsModelAdminMixin
from edc_lab_results.fieldsets import BloodResultFieldset, calculate_egfr_fieldset

from ...admin_site import effect_subject_admin
from ...forms import BloodResultsChemForm
from ...models import BloodResultsChem
from ..modeladmin import CrfModelAdmin


@admin.register(BloodResultsChem, site=effect_subject_admin)
class BloodResultsChemAdmin(BloodResultsModelAdminMixin, CrfModelAdmin):
    form = BloodResultsChemForm

    fieldsets = (
        *BloodResultFieldset(
            BloodResultsChem.lab_panel,
            model_cls=BloodResultsChem,
            extra_fieldsets=[
                (4, calculate_egfr_fieldset),
                (-1, action_fieldset_tuple),
            ],
            excluded_utest_ids=["egfr"],
        ).fieldsets,
    )

    def get_readonly_fields(self, request, obj=None) -> tuple[str, ...]:  # noqa: ARG002
        readonly_fields = super().get_readonly_fields(request)
        custom_fields = (
            "egfr_value",
            "egfr_units",
            "egfr_grade",
            "summary",
        )
        return tuple(set(custom_fields + readonly_fields))
