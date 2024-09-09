from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime
from typing import TYPE_CHECKING

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.sites.models import Site
from edc_appointment.constants import IN_PROGRESS_APPT, INCOMPLETE_APPT
from edc_appointment.tests.appointment_test_case_mixin import AppointmentTestCaseMixin
from edc_consent import site_consents
from edc_constants.constants import FEMALE, IN_PERSON, NEG, NO, NOT_APPLICABLE, POS, YES
from edc_facility.import_holidays import import_holidays
from edc_form_validators import FormValidatorTestCaseMixin
from edc_list_data.site_list_data import site_list_data
from edc_metadata import REQUIRED
from edc_metadata.models import CrfMetadata
from edc_randomization.site_randomizers import site_randomizers
from edc_sites.site import sites
from edc_sites.site import sites as site_sites
from edc_sites.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_sites.utils import add_or_update_django_sites
from edc_utils.date import get_utcnow, get_utcnow_as_date
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED
from model_bakery import baker

from effect_subject.models import SubjectVisit
from effect_visit_schedule.constants import DAY01
from effect_visit_schedule.visit_schedules import visit_schedule

from ..models import SubjectScreening

if TYPE_CHECKING:
    from effect_consent.models import SubjectConsent


def get_eligible_options() -> dict:
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
        cm_in_csf=NO,
        mg_severe_headache=NO,
        mg_headache_nuchal_rigidity=NO,
        mg_headache_vomiting=NO,
        mg_seizures=NO,
        mg_gcs_lt_15=NO,
        any_other_mg_ssx=NO,
        jaundice=NO,
        on_flucon=NO,
        pregnant=NOT_APPLICABLE,
        breast_feeding=NOT_APPLICABLE,
        prior_cm_episode=NO,
        reaction_to_study_drugs=NO,
    )


class EffectTestCaseMixin(
    AppointmentTestCaseMixin, FormValidatorTestCaseMixin, SiteTestCaseMixin
):
    default_sites = sites.get_by_country("tanzania", aslist=True)

    site_names = [s.name for s in default_sites]

    import_randomization_list = True

    sid_count = 10

    randomizer_name = "default"

    @classmethod
    def setUpTestData(cls):
        add_or_update_django_sites(single_sites=cls.default_sites)
        import_holidays(test=True)
        site_list_data.initialize()
        site_list_data.autodiscover()
        site_visit_schedules._registry = {}
        site_visit_schedules.register(visit_schedule=visit_schedule)
        randomizer_cls = site_randomizers.get(cls.randomizer_name)
        randomizer_cls.import_list(sid_count_for_tests=cls.sid_count)

    def get_subject_screening(
        self,
        report_datetime: datetime | None = None,
        eligibility_datetime: datetime | None = None,
        gender: str | None = None,
        age_in_years: int | None = None,
        cd4_date: date = None,
        serum_crag_date: date = None,
    ) -> SubjectScreening:
        eligible_options = deepcopy(get_eligible_options())
        if report_datetime:
            eligible_options.update(report_datetime=report_datetime)
        eligible_options["gender"] = gender or eligible_options["gender"]
        eligible_options["age_in_years"] = age_in_years or eligible_options["age_in_years"]
        eligible_options["cd4_date"] = cd4_date or eligible_options["cd4_date"]
        eligible_options["serum_crag_date"] = (
            serum_crag_date or eligible_options["serum_crag_date"]
        )

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
    def get_subject_consent(
        subject_screening: SubjectScreening,
        consent_datetime: datetime | None = None,
        site_id: int | None = None,
        dob: date | None = None,
    ) -> SubjectConsent:
        site = Site.objects.get(id=site_id or settings.SITE_ID)
        single_site = site_sites.get(site.id)
        consent_datetime = consent_datetime or subject_screening.report_datetime
        cdef = site_consents.get_consent_definition(
            site=single_site, report_datetime=consent_datetime
        )
        return baker.make_recipe(
            cdef.model,
            user_created="erikvw",
            user_modified="erikvw",
            screening_identifier=subject_screening.screening_identifier,
            initials=subject_screening.initials,
            gender=subject_screening.gender,
            dob=dob
            or (get_utcnow_as_date() - relativedelta(years=subject_screening.age_in_years)),
            site=site,
            consent_datetime=consent_datetime,
        )

    def get_subject_visit(
        self,
        visit_code: str | None = None,
        visit_code_sequence: int | None = None,
        subject_screening: SubjectScreening | None = None,
        subject_consent: SubjectConsent | None = None,
        reason: str | None = None,
        appt_datetime: datetime | None = None,
        gender: str | None = None,
        age_in_years: int | None = None,
        assessment_type: str | None = None,
    ) -> SubjectVisit:
        reason = reason or SCHEDULED
        subject_screening = subject_screening or self.get_subject_screening(
            gender=gender, age_in_years=age_in_years
        )
        dob = None
        if age_in_years:
            dob = get_utcnow() - relativedelta(years=age_in_years)
        subject_consent = subject_consent or self.get_subject_consent(
            subject_screening, dob=dob
        )
        options = dict(
            subject_identifier=subject_consent.subject_identifier,
            visit_code=visit_code or DAY01,
            visit_code_sequence=(
                visit_code_sequence if visit_code_sequence is not None else 0
            ),
            reason=reason,
        )
        if appt_datetime:
            options.update(appt_datetime=appt_datetime or subject_consent.consent_datetime)
        appointment = self.get_appointment(**options)
        return SubjectVisit.objects.create(
            appointment=appointment,
            reason=SCHEDULED,
            report_datetime=appointment.appt_datetime,
            assessment_type=assessment_type or IN_PERSON,
        )

    @staticmethod
    def get_next_subject_visit(
        subject_visit: SubjectVisit,
        assessment_type: str | None = None,
    ) -> SubjectVisit:
        appointment = subject_visit.appointment
        appointment.appt_status = INCOMPLETE_APPT
        appointment.save()
        appointment.refresh_from_db()
        next_appointment = appointment.next_by_timepoint
        next_appointment.appt_status = IN_PROGRESS_APPT
        next_appointment.save()
        return SubjectVisit.objects.create(
            appointment=next_appointment,
            reason=SCHEDULED,
            report_datetime=next_appointment.appt_datetime,
            assessment_type=assessment_type or IN_PERSON,
        )

    @staticmethod
    def get_crf_metadata(subject_visit: SubjectVisit) -> CrfMetadata:
        return CrfMetadata.objects.filter(
            subject_identifier=subject_visit.subject_identifier,
            visit_code=subject_visit.visit_code,
            visit_code_sequence=subject_visit.visit_code_sequence,
            entry_status=REQUIRED,
        )
