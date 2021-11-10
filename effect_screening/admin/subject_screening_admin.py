from django.contrib import admin
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django_audit_fields.admin import audit_fieldset_tuple
from edc_dashboard.url_names import url_names
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from ..admin_site import effect_screening_admin
from ..eligibility import Eligibility, format_reasons_ineligible
from ..forms import SubjectScreeningForm
from ..models import SubjectScreening


@admin.register(SubjectScreening, site=effect_screening_admin)
class SubjectScreeningAdmin(ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin):

    form = SubjectScreeningForm

    post_url_on_delete_name = "screening_listboard_url"
    subject_listboard_url_name = "screening_listboard_url"

    additional_instructions = (
        "Patients must meet ALL of the inclusion criteria and NONE of the "
        "exclusion criteria in order to proceed to the final screening stage"
    )

    fieldsets = (
        [
            None,
            {
                "fields": (
                    "report_datetime",
                    "screening_consent",
                    "willing_to_participate",
                    "capable_to_consent",
                ),
            },
        ],
        ["Demographics", {"fields": ("initials", "gender", "age_in_years")}],
        [
            "Criteria",
            {
                "fields": (
                    "hiv_pos",
                    "cd4_value",
                    "cd4_date",
                    "pregnant_or_bf",
                    "crag_value",
                    "lp_status",
                    "csf_crag_value",
                    "prior_cm_epidose",
                    "prior_cm_epidose_date",
                    "reaction_to_study_drugs",
                    "on_fluconazole",
                    "contraindicated_meds",
                    "meningitis_symptoms",
                    "jaundice",
                    "csf_value",
                    "csf_date",
                ),
            },
        ],
        [
            "Additional Comments",
            {
                "fields": (
                    "unsuitable_for_study",
                    "reasons_unsuitable",
                    "unsuitable_agreed",
                ),
            },
        ],
        audit_fieldset_tuple,
    )

    radio_fields = {
        "screening_consent": admin.VERTICAL,
        "willing_to_participate": admin.VERTICAL,
        "capable_to_consent": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "hiv_pos": admin.VERTICAL,
        "pregnant_or_bf": admin.VERTICAL,
        "crag_value": admin.VERTICAL,
        "csf_crag_value": admin.VERTICAL,
        "csf_value": admin.VERTICAL,
        "lp_status": admin.VERTICAL,
        "prior_cm_epidose": admin.VERTICAL,
        "reaction_to_study_drugs": admin.VERTICAL,
        "on_fluconazole": admin.VERTICAL,
        "contraindicated_meds": admin.VERTICAL,
        "meningitis_symptoms": admin.VERTICAL,
        "jaundice": admin.VERTICAL,
        "unsuitable_agreed": admin.VERTICAL,
        "unsuitable_for_study": admin.VERTICAL,
    }

    list_display = (
        "screening_identifier",
        "eligiblity_status",
        "demographics",
        "reasons",
        "report_datetime",
        "user_created",
        "created",
    )

    list_filter = (
        "report_datetime",
        "gender",
        "eligible",
        "consented",
        "refused",
    )

    search_fields = (
        "screening_identifier",
        "subject_identifier",
        "initials",
        "reasons_ineligible",
    )

    # readonly_fields = ()

    def post_url_on_delete_kwargs(self, request, obj):
        return {}

    @staticmethod
    def demographics(obj=None):
        return mark_safe(
            f"{obj.get_gender_display()} {obj.age_in_years}yrs<BR>"
            f"Initials: {obj.initials.upper()}<BR><BR>"
        )

    @staticmethod
    def reasons(obj=None):
        return format_reasons_ineligible(obj.reasons_ineligible)

    @staticmethod
    def eligiblity_status(obj=None):
        eligibility = Eligibility(obj)
        return mark_safe(eligibility.eligibility_status)

    def dashboard(self, obj=None, label=None):
        try:
            url = reverse(
                self.get_subject_dashboard_url_name(),
                kwargs=self.get_subject_dashboard_url_kwargs(obj),
            )
        except NoReverseMatch:
            url = reverse(url_names.get("screening_listboard_url"), kwargs={})
            context = dict(
                title=_("Go to screening listboard"),
                url=f"{url}?q={obj.screening_identifier}",
                label=label,
            )
        else:
            context = dict(title=_("Go to subject dashboard"), url=url, label=label)
        return render_to_string("dashboard_button.html", context=context)
