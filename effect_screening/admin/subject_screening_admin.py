from django.contrib import admin
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django_audit_fields.admin import audit_fieldset_tuple
from edc_dashboard.url_names import url_names
from edc_model_admin import SimpleHistoryAdmin
from edc_model_admin.dashboard import ModelAdminSubjectDashboardMixin

from effect_screening.eligibility import ScreeningEligibility

from ..admin_site import effect_screening_admin
from ..forms import SubjectScreeningForm
from ..models import SubjectScreening


@admin.register(SubjectScreening, site=effect_screening_admin)
class SubjectScreeningAdmin(ModelAdminSubjectDashboardMixin, SimpleHistoryAdmin):

    form = SubjectScreeningForm

    post_url_on_delete_name = "screening_listboard_url"
    subject_listboard_url_name = "screening_listboard_url"

    additional_instructions = (
        "Patients must meet ALL of the inclusion criteria and NONE of the "
        "exclusion criteria in order to be considered eligible for enrolment"
    )

    fieldsets = (
        [
            None,
            {
                "fields": (
                    "screening_identifier",
                    "report_datetime",
                    "willing_to_participate",
                    "consent_ability",
                ),
            },
        ],
        ["Demographics", {"fields": ("initials", "gender", "age_in_years")}],
        [
            "HIV / CD4",
            {
                "fields": (
                    "hiv_pos",
                    "cd4_value",
                    "cd4_date",
                ),
            },
        ],
        [
            "Serum CrAg",
            {
                "fields": (
                    "serum_crag_value",
                    "serum_crag_date",
                ),
            },
        ],
        [
            "LP / CSF CrAg",
            {
                "fields": (
                    "lp_done",
                    "lp_date",
                    "lp_declined",
                    "csf_crag_value",
                ),
            },
        ],
        [
            "Treatment",
            {
                "fields": (
                    "reaction_to_study_drugs",
                    "on_fluconazole",
                    "contraindicated_meds",
                ),
            },
        ],
        [
            "Other evidence of CM on CSF",
            {
                "description": format_html(
                    "<H3>Note: for evidence of CM on CSF, consider, for example, "
                    "positive microscopy with India Ink, culture, or CrAg test) at any "
                    "time between the CrAg test and screening for eligibility, or during the "
                    "first 2 weeks of antifungal treatment, while the patient remained "
                    "without clinical signs or symptoms of meningitis as described above. "
                    "(late withdrawal criterion).</H3>"
                ),
                "fields": (
                    "csf_cm_evidence",
                    "csf_results_date",
                    "prior_cm_epidose",
                ),
            },
        ],
        [
            "Additional exclusion criteria",
            {
                "description": format_html(
                    "<div><H3>Note: for signs of meningitis below, consider, for example: "
                    "<BR> * a progressively severe headache OR;"
                    "<BR> * a headache and marked nuchal rigidity OR;"
                    "<BR> * a headache and vomiting OR;"
                    "<BR> * seizures OR;"
                    "<BR> * a Glasgow Coma Scale (GCS) score of &lt15</H3>"
                ),
                "fields": (
                    "meningitis_symptoms",
                    "jaundice",
                    "pregnant_or_bf",
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
        [
            "Eligibility",
            {
                "classes": ("collapse",),
                "fields": (
                    "subject_identifier",
                    "eligible",
                    "eligibility_datetime",
                    "real_eligibility_datetime",
                    "reasons_ineligible",
                    "consented",
                    "refused",
                ),
            },
        ],
        audit_fieldset_tuple,
    )

    radio_fields = {
        "consent_ability": admin.VERTICAL,
        "contraindicated_meds": admin.VERTICAL,
        "csf_cm_evidence": admin.VERTICAL,
        "csf_crag_value": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "hiv_pos": admin.VERTICAL,
        "jaundice": admin.VERTICAL,
        "lp_declined": admin.VERTICAL,
        "lp_done": admin.VERTICAL,
        "meningitis_symptoms": admin.VERTICAL,
        "on_fluconazole": admin.VERTICAL,
        "pregnant_or_bf": admin.VERTICAL,
        "prior_cm_epidose": admin.VERTICAL,
        "reaction_to_study_drugs": admin.VERTICAL,
        "serum_crag_value": admin.VERTICAL,
        "unsuitable_agreed": admin.VERTICAL,
        "unsuitable_for_study": admin.VERTICAL,
        "willing_to_participate": admin.VERTICAL,
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

    readonly_fields = [
        "screening_identifier",
        "subject_identifier",
        "eligible",
        "eligibility_datetime",
        "real_eligibility_datetime",
        "reasons_ineligible",
        "consented",
        "refused",
    ]

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
        return ScreeningEligibility(obj)

    @staticmethod
    def eligiblity_status(obj=None):
        eligibility = ScreeningEligibility(obj)
        return mark_safe(eligibility.eligibility_display_label)

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
