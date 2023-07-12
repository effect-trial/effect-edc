from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_constants.constants import YES
from edc_metadata.metadata_rules import PredicateCollection
from edc_visit_schedule.constants import DAY01


def screening_lp_performed(subject_identifier: str):
    screening_model_cls = django_apps.get_model("effect_screening.subjectscreening")
    try:
        screening_model_cls.objects.get(
            subject_identifier=subject_identifier,
            lp_done=YES,
        )
    except ObjectDoesNotExist:
        return False
    return True


class Predicates(PredicateCollection):
    app_label = "effect_subject"
    visit_model = "effect_subject.subjectvisit"

    def lpcsf_crf_required(self, visit, **kwargs) -> bool:
        """Require at baseline if screening form indicates a screening LP was
        performed. Otherwise, require for ANY visit where SiSx form indicates a
        diagnosis LP was performed.
        """

        required = (
            visit.appointment.visit_code == DAY01
            and visit.appointment.visit_code_sequence == 0
            and screening_lp_performed(subject_identifier=visit.subject_identifier)
        )

        model_cls = django_apps.get_model(f"{self.app_label}.signsandsymptoms")
        try:
            model_cls.objects.get(
                subject_visit__subject_identifier=visit.subject_identifier,
                subject_visit__visit_code=visit.appointment.visit_code,
                subject_visit__visit_code_sequence=visit.appointment.visit_code_sequence,
                lp_performed=YES,
            )
        except ObjectDoesNotExist:
            pass
        else:
            required = True
        return required
