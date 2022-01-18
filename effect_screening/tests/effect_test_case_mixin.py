from copy import deepcopy

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.sites.models import Site
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.tests.appointment_test_case_mixin import AppointmentTestCaseMixin
from edc_constants.constants import FEMALE, NEG, NO, NOT_APPLICABLE, POS, YES
from edc_facility.import_holidays import import_holidays
from edc_form_validators import FormValidatorTestCaseMixin
from edc_list_data.site_list_data import site_list_data
from edc_metadata import REQUIRED
from edc_metadata.models import CrfMetadata
from edc_sites import add_or_update_django_sites, get_sites_by_country
from edc_sites.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_utils.date import get_utcnow
from edc_visit_schedule.constants import DAY1
from edc_visit_tracking.constants import SCHEDULED
from model_bakery import baker

from effect_sites import fqdn
from effect_subject.models import SubjectVisit

from ..models import SubjectScreening


def get_eligible_options():
    return dict(
        screening_consent=YES,
        willing_to_participate=YES,
        consent_ability=YES,
        report_datetime=get_utcnow(),
        initials="EW",
        gender=FEMALE,
        age_in_years=25,
        unsuitable_for_study=NO,
        unsuitable_agreed=NOT_APPLICABLE,
        hiv_pos=YES,
        cd4_value=99,
        cd4_date=(get_utcnow() - relativedelta(days=7)).date(),
        serum_crag_value=POS,
        serum_crag_date=(get_utcnow() - relativedelta(days=6)).date(),
        lp_declined=NOT_APPLICABLE,
        lp_done=YES,
        lp_date=(get_utcnow() - relativedelta(days=6)).date(),
        csf_crag_value=NEG,
        contraindicated_meds=NO,
        csf_cm_evidence=NO,
        jaundice=NO,
        meningitis_symptoms=NO,
        on_fluconazole=NO,
        pregnant_or_bf=NOT_APPLICABLE,
        prior_cm_epidose=NO,
        reaction_to_study_drugs=NO,
    )


class EffectTestCaseMixin(
    AppointmentTestCaseMixin, FormValidatorTestCaseMixin, SiteTestCaseMixin
):

    fqdn = fqdn

    default_sites = get_sites_by_country("tanzania")

    site_names = [s.name for s in default_sites]

    import_randomization_list = True

    sid_count = 10

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        add_or_update_django_sites(sites=get_sites_by_country("tanzania"))
        import_holidays(test=True)
        site_list_data.initialize()
        site_list_data.autodiscover()

    def get_subject_screening(
        self,
        report_datetime=None,
        eligibility_datetime=None,
        gender=None,
    ):
        eligible_options = deepcopy(get_eligible_options())
        if report_datetime:
            eligible_options.update(report_datetime=report_datetime)
        eligible_options["gender"] = gender or eligible_options["gender"]

        subject_screening = SubjectScreening.objects.create(
            user_created="erikvw", user_modified="erikvw", **eligible_options
        )

        screening_identifier = subject_screening.screening_identifier
        self.assertIsNone(subject_screening.reasons_ineligible)
        self.assertTrue(subject_screening.eligible)

        subject_screening = SubjectScreening.objects.get(
            screening_identifier=screening_identifier
        )

        self.assertTrue(subject_screening.eligible)

        if eligibility_datetime:
            subject_screening.eligibility_datetime = eligibility_datetime
            subject_screening.save()
            subject_screening = SubjectScreening.objects.get(
                screening_identifier=screening_identifier
            )
        return subject_screening

    @staticmethod
    def get_subject_consent(subject_screening, consent_datetime=None, site_id=None):
        return baker.make_recipe(
            "effect_consent.subjectconsent",
            user_created="erikvw",
            user_modified="erikvw",
            screening_identifier=subject_screening.screening_identifier,
            initials=subject_screening.initials,
            gender=subject_screening.gender,
            dob=(
                get_utcnow().date()
                - relativedelta(years=subject_screening.age_in_years)
            ),
            site=Site.objects.get(id=site_id or settings.SITE_ID),
            consent_datetime=consent_datetime or subject_screening.report_datetime,
        )

    def get_subject_visit(
        self,
        visit_code=None,
        visit_code_sequence=None,
        subject_screening=None,
        subject_consent=None,
        reason=None,
        appt_datetime=None,
        gender=None,
    ):
        reason = reason or SCHEDULED
        subject_screening = subject_screening or self.get_subject_screening(
            gender=gender
        )
        subject_consent = subject_consent or self.get_subject_consent(subject_screening)
        options = dict(
            subject_identifier=subject_consent.subject_identifier,
            visit_code=visit_code or DAY1,
            visit_code_sequence=(
                visit_code_sequence if visit_code_sequence is not None else 0
            ),
            reason=reason,
        )
        if appt_datetime:
            options.update(appt_datetime=appt_datetime)
        appointment = self.get_appointment(**options)
        return SubjectVisit.objects.create(appointment=appointment, reason=SCHEDULED)

    @staticmethod
    def get_next_subject_visit(subject_visit):
        appointment = subject_visit.appointment
        appointment.appt_status = INCOMPLETE_APPT
        appointment.save()
        appointment.refresh_from_db()
        next_appointment = appointment.next_by_timepoint
        next_appointment.appt_status = IN_PROGRESS_APPT
        next_appointment.save()
        return SubjectVisit.objects.create(
            appointment=next_appointment, reason=SCHEDULED
        )

    @staticmethod
    def get_crf_metadata(subject_visit):
        return CrfMetadata.objects.filter(
            subject_identifier=subject_visit.subject_identifier,
            visit_code=subject_visit.visit_code,
            visit_code_sequence=subject_visit.visit_code_sequence,
            entry_status=REQUIRED,
        )

    def assertFieldFormValidationErrorRaised(
        self,
        form_validator,
        field: str,
        expected_msg: str,
        expected_errors: int = 1,
    ):
        self.assertIn(
            field,
            form_validator._errors,
            msg=(
                f"Expected to find field '{field}' "
                f"listed in the form validation errors: '{form_validator._errors}'"
            ),
        )
        self.assertIn(
            expected_msg,
            str(form_validator._errors.get(field)),
            msg=(
                f"Expected to find error message '{expected_errors}' "
                f"in form validation errors: '{form_validator._errors}'"
            ),
        )
        self.assertEqual(
            len(form_validator._errors),
            expected_errors,
            msg=(
                f"Expected {expected_errors} error message(s) in form validator, "
                f"but got {len(form_validator._errors)}, "
                f"as follows: '{form_validator._errors}'"
            ),
        )
