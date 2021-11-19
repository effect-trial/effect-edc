import pdb
from copy import deepcopy

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.sites.models import Site
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.tests.appointment_test_case_mixin import AppointmentTestCaseMixin
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from edc_facility.models import Holiday
from edc_list_data.site_list_data import site_list_data
from edc_metadata import REQUIRED
from edc_metadata.models import CrfMetadata
from edc_randomization.site_randomizers import site_randomizers
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
    return dict()


class EffectTestCaseMixin(AppointmentTestCaseMixin, SiteTestCaseMixin):

    fqdn = fqdn

    default_sites = get_sites_by_country("tanzania")

    site_names = [s.name for s in default_sites]

    import_randomization_list = True

    sid_count = 10

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        add_or_update_django_sites(sites=get_sites_by_country("tanzania"))
        # site_randomizers._registry = {}
        # if cls.import_randomization_list:
        #     site_randomizers.register(Randomizer)
        #     Randomizer.import_list(
        #         verbose=False, sid_count_for_tests=cls.sid_count
        #     )
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
        self.assertEqual(subject_screening.eligible, YES)

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
            "meta_consent.subjectconsent",
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