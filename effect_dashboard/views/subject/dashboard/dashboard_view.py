from edc_randomization.utils import (
    get_assignment_description_for_subject,
    get_assignment_for_subject,
)
from edc_subject_dashboard.views import SubjectDashboardView


class DashboardView(SubjectDashboardView):

    consent_model = "effect_consent.subjectconsent"
    navbar_selected_item = "consented_subject"
    visit_model = "effect_subject.subjectvisit"
    history_button_label = "Audit"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            assignment=get_assignment_for_subject(
                subject_identifier=self.kwargs.get("subject_identifier"),
                randomizer_name="default",
            ),
            assignment_description=get_assignment_description_for_subject(
                subject_identifier=self.kwargs.get("subject_identifier"),
                randomizer_name="default",
            ),
        )
        return context
