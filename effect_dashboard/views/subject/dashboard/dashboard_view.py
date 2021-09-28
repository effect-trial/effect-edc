from edc_subject_dashboard.views import SubjectDashboardView


class DashboardView(SubjectDashboardView):

    consent_model = "effect_consent.subjectconsent"
    navbar_selected_item = "consented_subject"
    visit_model = "effect_subject.subjectvisit"
