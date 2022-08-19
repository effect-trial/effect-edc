from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import CONTROL, INTERVENTION
from edc_subject_dashboard.views import SubjectDashboardView


class InvalidAssignment(Exception):
    pass


class SubjectNotRandomized(Exception):
    pass


class DashboardView(SubjectDashboardView):

    consent_model = "effect_consent.subjectconsent"
    navbar_selected_item = "consented_subject"
    visit_model = "effect_subject.subjectvisit"

    @property
    def assignment(self):
        model_cls = django_apps.get_model("edc_randomization.randomizationlist")
        subject_identifier = self.kwargs.get("subject_identifier")
        try:
            obj = model_cls.objects.get(subject_identifier=subject_identifier)
        except ObjectDoesNotExist as e:
            raise SubjectNotRandomized(f"Subject {subject_identifier} not found. Got {e}")
        return obj.assignment

    def get_context_data(self, **kwargs):
        if self.assignment == INTERVENTION:
            assignment_description = "2 weeks fluconazole plus flucytosine"
        elif self.assignment == CONTROL:
            assignment_description = "2 weeks fluconazole alone"
        else:
            raise InvalidAssignment(f"Invalid assignment.  Got {self.assignment}")

        context = super().get_context_data(**kwargs)
        context.update(
            assignment=self.assignment,
            assignment_description=assignment_description,
        )
        return context
