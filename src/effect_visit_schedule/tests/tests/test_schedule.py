from datetime import datetime
from zoneinfo import ZoneInfo

from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_visit_schedule.constants import VISIT_SCHEDULE


@tag("vsched")
class TestVisitSchedule(TestCase):
    def test_visit_schedule_models(self):
        visit_schedules = site_visit_schedules.get_visit_schedules(VISIT_SCHEDULE)
        self.assertEqual(len(visit_schedules), 1)
        for visit_schedule in visit_schedules.values():
            self.assertEqual(visit_schedule.death_report_model, "effect_ae.deathreport")
            self.assertEqual(visit_schedule.offstudy_model, "edc_offstudy.subjectoffstudy")
            self.assertEqual(visit_schedule.locator_model, "edc_locator.subjectlocator")

    def test_schedule_models(self):
        visit_schedules = site_visit_schedules.get_visit_schedules(VISIT_SCHEDULE)
        for visit_schedule in visit_schedules.values():
            for schedule in visit_schedule.schedules.values():
                self.assertEqual(schedule.onschedule_model, "effect_prn.onschedule")
                self.assertEqual(schedule.offschedule_model, "effect_prn.endofstudy")
                self.assertEqual(len(schedule.consent_definitions), 2)
                self.assertEqual(
                    schedule.consent_definitions[0].model, "effect_consent.subjectconsentv1"
                )
                self.assertEqual(schedule.appointment_model, "edc_appointment.appointment")

    def test_visit_codes(self):
        visit_schedules = site_visit_schedules.get_visit_schedules(VISIT_SCHEDULE)
        for visit_schedule in visit_schedules.values():
            for schedule in visit_schedule.schedules.values():
                self.assertEqual(
                    [
                        "1000",
                        "1003",
                        "1009",
                        "1014",
                        "1028",
                        "1070",
                        "1112",
                        "1168",
                    ],
                    [visit for visit in schedule.visits],
                )

    def test_requisitions(self):
        visit_schedules = site_visit_schedules.get_visit_schedules(VISIT_SCHEDULE)
        for visit_schedule in visit_schedules.values():
            for schedule in visit_schedule.schedules.values():
                prn = [
                    "blood_culture",
                    "csf_culture",
                    "fbc",
                    "sputum",
                    "tissue_biopsy",
                    "chemistry",
                ]
                expected = {
                    "1000": [
                        "fbc",
                        "chemistry",
                    ],
                    "1003": [],
                    "1009": [],
                    "1014": ["fbc"],
                    "1028": [],
                    "1070": [],
                    "1112": [],
                    "1168": [],
                }
                for visit_code, visit in schedule.visits.items():
                    with self.subTest(visit_code=visit_code, visit=visit):
                        actual = [requisition.name for requisition in visit.requisitions]
                        actual.sort()
                        expected_for_visit = expected.get(visit_code)
                        expected_for_visit.sort()
                        self.assertEqual(
                            expected_for_visit,
                            actual,
                            msg=f"see requisitions for visit {visit_code}",
                        )
                        actual = [requisition.name for requisition in visit.requisitions_prn]
                        actual.sort()
                        prn.sort()
                        self.assertEqual(
                            prn, actual, msg=f"see PRN requisitions for visit {visit_code}"
                        )

    def test_crfs(self):
        visit_schedules = site_visit_schedules.get_visit_schedules(VISIT_SCHEDULE)
        for visit_schedule in visit_schedules.values():
            for schedule in visit_schedule.schedules.values():
                prn_baseline = [
                    "effect_subject.vitalsigns",
                    "effect_subject.bloodculture",
                    "effect_subject.bloodresultsfbc",
                    "effect_subject.bloodresultschem",
                    "effect_subject.healtheconomicsevent",
                    "effect_subject.histopathology",
                    "effect_subject.chestxray",
                    "effect_subject.lpcsf",
                    "effect_subject.tbdiagnostics",
                    "effect_subject.clinicalnote",
                ]
                prn_followup = prn_baseline + ["effect_subject.studymedicationfollowup"]
                expected = {
                    "1000": [
                        "effect_subject.arvhistory",
                        "effect_subject.participanthistory",
                        "effect_subject.vitalsigns",
                        "effect_subject.mentalstatus",
                        "effect_subject.signsandsymptoms",
                        "effect_subject.studymedicationbaseline",
                        "effect_subject.bloodresultsfbc",
                        "effect_subject.bloodresultschem",
                        "effect_subject.chestxray",
                        "effect_subject.lpcsf",
                        "effect_subject.tbdiagnostics",
                        "effect_subject.healtheconomics",
                        "effect_subject.clinicalnote",
                        "effect_subject.adherencestageone",
                    ],
                    "1003": [
                        "effect_subject.vitalsigns",
                        "effect_subject.mentalstatus",
                        "effect_subject.signsandsymptoms",
                        "effect_subject.diagnoses",
                        "effect_subject.chestxray",
                        "effect_subject.lpcsf",
                        "effect_subject.tbdiagnostics",
                        "effect_subject.adherencestagetwo",
                    ],
                    "1009": [
                        "effect_subject.vitalsigns",
                        "effect_subject.mentalstatus",
                        "effect_subject.signsandsymptoms",
                        "effect_subject.diagnoses",
                        "effect_subject.chestxray",
                        "effect_subject.lpcsf",
                        "effect_subject.tbdiagnostics",
                        "effect_subject.adherencestagetwo",
                    ],
                    "1014": [
                        "effect_subject.studymedicationfollowup",
                        "effect_subject.vitalsigns",
                        "effect_subject.mentalstatus",
                        "effect_subject.signsandsymptoms",
                        "effect_subject.diagnoses",
                        "effect_subject.arvtreatment",
                        "effect_subject.participanttreatment",
                        "effect_subject.bloodresultsfbc",
                        "effect_subject.chestxray",
                        "effect_subject.lpcsf",
                        "effect_subject.tbdiagnostics",
                        "effect_subject.clinicalnote",
                        "effect_subject.adherencestagethree",
                    ],
                    "1028": [
                        "effect_subject.vitalsigns",
                        "effect_subject.mentalstatus",
                        "effect_subject.signsandsymptoms",
                        "effect_subject.diagnoses",
                        "effect_subject.chestxray",
                        "effect_subject.lpcsf",
                        "effect_subject.tbdiagnostics",
                        "effect_subject.adherencestagefour",
                    ],
                    "1070": [
                        "effect_subject.vitalsigns",
                        "effect_subject.studymedicationfollowup",
                        "effect_subject.mentalstatus",
                        "effect_subject.signsandsymptoms",
                        "effect_subject.diagnoses",
                        "effect_subject.chestxray",
                        "effect_subject.lpcsf",
                        "effect_subject.tbdiagnostics",
                        "effect_subject.adherencestagefour",
                    ],
                    "1112": [
                        "effect_subject.vitalsigns",
                        "effect_subject.mentalstatus",
                        "effect_subject.signsandsymptoms",
                        "effect_subject.diagnoses",
                        "effect_subject.chestxray",
                        "effect_subject.lpcsf",
                        "effect_subject.tbdiagnostics",
                        "effect_subject.adherencestagefour",
                    ],
                    "1168": [
                        "effect_subject.vitalsigns",
                        "effect_subject.mentalstatus",
                        "effect_subject.signsandsymptoms",
                        "effect_subject.diagnoses",
                        "effect_subject.chestxray",
                        "effect_subject.lpcsf",
                        "effect_subject.tbdiagnostics",
                        "effect_subject.healtheconomics",
                        "effect_subject.adherencestagefour",
                    ],
                }
                prn_baseline.sort()
                prn_followup.sort()

                for visit_code, visit in schedule.visits.items():
                    with self.subTest(visit_code=visit_code, visit=visit):
                        # CRFs
                        actual_crfs = [crf.model for crf in visit.crfs]
                        actual_crfs.sort()
                        expected.get(visit_code).sort()
                        expected_crfs = expected.get(visit_code)
                        self.assertEqual(
                            actual_crfs,
                            expected_crfs,
                            msg=f"see CRFs for visit {visit_code}"
                            f"\nExpected: \n{expected_crfs}. \nGot: \n{actual_crfs}",
                        )

                        # PRNs
                        actual_prns = [crf.model for crf in visit.crfs_prn]
                        actual_prns.sort()
                        expected_prns = prn_baseline if visit_code == "1000" else prn_followup
                        self.assertEqual(
                            prn_baseline if visit_code == "1000" else prn_followup,
                            actual_prns,
                            msg=f"see PRN CRFs for visit {visit_code}. "
                            f"\nExpected: \n{expected_prns}. \nGot: \n{actual_prns}",
                        )

    def test_crfs_unscheduled(self):
        visit_schedules = site_visit_schedules.get_visit_schedules(VISIT_SCHEDULE)
        for visit_schedule in visit_schedules.values():
            for schedule in visit_schedule.schedules.values():
                prn_baseline = [
                    "effect_subject.vitalsigns",
                    "effect_subject.bloodculture",
                    "effect_subject.bloodresultsfbc",
                    "effect_subject.bloodresultschem",
                    "effect_subject.healtheconomicsevent",
                    "effect_subject.histopathology",
                    "effect_subject.chestxray",
                    "effect_subject.lpcsf",
                    "effect_subject.tbdiagnostics",
                    "effect_subject.clinicalnote",
                ]
                prn_followup = prn_baseline + ["effect_subject.studymedicationfollowup"]
                crfs_unscheduled = [
                    "effect_subject.vitalsigns",
                    "effect_subject.mentalstatus",
                    "effect_subject.signsandsymptoms",
                    "effect_subject.diagnoses",
                    "effect_subject.healtheconomicsevent",
                    "effect_subject.clinicalnote",
                ]
                expected = {
                    "1000": crfs_unscheduled + ["effect_subject.adherencestagetwo"],
                    "1003": crfs_unscheduled + ["effect_subject.adherencestagetwo"],
                    "1009": crfs_unscheduled + ["effect_subject.adherencestagetwo"],
                    "1014": crfs_unscheduled + ["effect_subject.adherencestagefour"],
                    "1028": crfs_unscheduled + ["effect_subject.adherencestagefour"],
                    "1070": crfs_unscheduled + ["effect_subject.adherencestagefour"],
                    "1112": crfs_unscheduled + ["effect_subject.adherencestagefour"],
                    "1168": crfs_unscheduled + ["effect_subject.adherencestagefour"],
                }
                prn_baseline.sort()
                prn_followup.sort()

                for visit_code, visit in schedule.visits.items():
                    with self.subTest(visit_code=visit_code, visit=visit):
                        # Unscheduled CRFs
                        actual_crfs = [crf.model for crf in visit.crfs_unscheduled]
                        actual_crfs.sort()
                        expected.get(visit_code).sort()
                        expected_crfs = expected.get(visit_code)
                        self.assertEqual(
                            expected_crfs,
                            actual_crfs,
                            msg=f"see CRFs for visit {visit_code}"
                            f"\nExpected: \n{expected_crfs}. \nGot: \n{actual_crfs}",
                        )

                        # PRNs
                        actual_prns = [crf.model for crf in visit.crfs_prn]
                        actual_prns.sort()
                        expected_prns = prn_baseline if visit_code == "1000" else prn_followup

                        self.assertEqual(
                            expected_prns,
                            actual_prns,
                            msg=f"see PRN CRFs for visit {visit_code}"
                            f"\nExpected: \n{expected_prns}. \nGot: \n{actual_prns}",
                        )

    def test_crfs_missed(self):
        visit_schedules = site_visit_schedules.get_visit_schedules(VISIT_SCHEDULE)
        for visit_schedule in visit_schedules.values():
            for schedule in visit_schedule.schedules.values():
                expected_crfs = ["effect_subject.subjectvisitmissed"]
                for visit_code, visit in schedule.visits.items():
                    with self.subTest(visit_code=visit_code, visit=visit):
                        actual_crfs = [crf.model for crf in visit.crfs_missed]
                        actual_crfs.sort()
                        self.assertEqual(
                            expected_crfs,
                            actual_crfs,
                            msg=f"see CRFs for visit {visit_code}"
                            f"\nExpected: \n{expected_crfs}. \nGot: \n{actual_crfs}",
                        )


@tag("vsched")
class TestVisitScheduleDates(EffectTestCaseMixin, TestCase):
    def test_generated_visit_dates_against_dates_relative_to_consent(self):
        consent_date = get_utcnow()
        expected_appts = {
            "1000": consent_date,
            "1003": consent_date + relativedelta(days=3 - 1),
            "1009": consent_date + relativedelta(days=9 - 1),
            "1014": consent_date + relativedelta(days=14 - 1),
            "1028": consent_date + relativedelta(weeks=4),
            "1070": consent_date + relativedelta(weeks=10),
            "1112": consent_date + relativedelta(weeks=16),
            "1168": consent_date + relativedelta(weeks=24),
        }

        visits = self.get_subject_visit().visits.timepoint_dates(dt=consent_date)
        for visit in visits:
            with self.subTest(visit_code=visit.code):
                self.assertEqual(visit.timepoint_datetime, expected_appts.get(visit.code))

        actual = {visit.code: visit.dates.base for visit in visits}
        self.assertDictEqual(expected_appts, actual)

    def test_generated_visit_dates_against_absolute_dates(self):
        consent_date = datetime(year=2022, month=3, day=9, hour=9, tzinfo=ZoneInfo("UTC"))
        expected_appts = {
            "1000": consent_date,
            "1003": datetime(year=2022, month=3, day=11, hour=9, tzinfo=ZoneInfo("UTC")),
            "1009": datetime(year=2022, month=3, day=17, hour=9, tzinfo=ZoneInfo("UTC")),
            "1014": datetime(year=2022, month=3, day=22, hour=9, tzinfo=ZoneInfo("UTC")),
            "1028": datetime(year=2022, month=4, day=6, hour=9, tzinfo=ZoneInfo("UTC")),
            "1070": datetime(year=2022, month=5, day=18, hour=9, tzinfo=ZoneInfo("UTC")),
            "1112": datetime(year=2022, month=6, day=29, hour=9, tzinfo=ZoneInfo("UTC")),
            "1168": datetime(year=2022, month=8, day=24, hour=9, tzinfo=ZoneInfo("UTC")),
        }

        visits = self.get_subject_visit().visits.timepoint_dates(dt=consent_date)
        for visit in visits:
            with self.subTest(visit_code=visit.code):
                self.assertEqual(visit.timepoint_datetime, expected_appts.get(visit.code))

        actual = {visit.code: visit.dates.base for visit in visits}
        self.assertDictEqual(expected_appts, actual)

    def test_visit_window_floors_against_dates_relative_to_consent(self):
        consent_date = get_utcnow()
        expected_visit_window_floors = {
            "1000": consent_date,
            "1003": consent_date
            + relativedelta(days=2 - 1, hour=0, minute=0, second=0, microsecond=0),
            "1009": consent_date
            + relativedelta(days=8 - 1, hour=0, minute=0, second=0, microsecond=0),
            "1014": consent_date
            + relativedelta(days=14 - 1, hour=0, minute=0, second=0, microsecond=0),
            "1028": consent_date
            + relativedelta(days=22 - 1, hour=0, minute=0, second=0, microsecond=0),
            "1070": consent_date
            + relativedelta(days=64 - 1, hour=0, minute=0, second=0, microsecond=0),
            "1112": consent_date
            + relativedelta(days=106 - 1, hour=0, minute=0, second=0, microsecond=0),
            "1168": consent_date
            + relativedelta(days=162 - 1, hour=0, minute=0, second=0, microsecond=0),
        }

        visits = self.get_subject_visit().visits.timepoint_dates(dt=consent_date)
        for visit in visits:
            with self.subTest(visit_code=visit.code):
                expected_visit_floor = expected_visit_window_floors.get(visit.code)
                self.assertEqual(visit.dates.lower, expected_visit_floor)

    def test_visit_window_floors_against_absolute_dates(self):
        consent_date = datetime(
            year=2022, month=3, day=9, hour=9, minute=25, tzinfo=ZoneInfo("UTC")
        )
        expected_visit_window_floors = {
            "1000": consent_date,
            "1003": datetime(year=2022, month=3, day=10, tzinfo=ZoneInfo("UTC")),
            "1009": datetime(year=2022, month=3, day=16, tzinfo=ZoneInfo("UTC")),
            "1014": datetime(year=2022, month=3, day=22, tzinfo=ZoneInfo("UTC")),
            "1028": datetime(year=2022, month=3, day=30, tzinfo=ZoneInfo("UTC")),
            "1070": datetime(year=2022, month=5, day=11, tzinfo=ZoneInfo("UTC")),
            "1112": datetime(year=2022, month=6, day=22, tzinfo=ZoneInfo("UTC")),
            "1168": datetime(year=2022, month=8, day=17, tzinfo=ZoneInfo("UTC")),
        }

        visits = self.get_subject_visit().visits.timepoint_dates(dt=consent_date)
        for visit in visits:
            with self.subTest(visit_code=visit.code):
                expected_visit_floor = expected_visit_window_floors.get(visit.code)
                self.assertEqual(visit.dates.lower, expected_visit_floor)

    def test_visit_window_ceilings_against_dates_relative_to_consent(self):
        consent_date = get_utcnow()
        expected_visit_window_ceilings = {
            "1000": consent_date.replace(hour=23, minute=59, second=59, microsecond=999999),
            "1003": consent_date
            + relativedelta(days=7 - 1, hour=23, minute=59, second=59, microsecond=999999),
            "1009": consent_date
            + relativedelta(days=13 - 1, hour=23, minute=59, second=59, microsecond=999999),
            "1014": consent_date
            + relativedelta(days=21 - 1, hour=23, minute=59, second=59, microsecond=999999),
            "1028": consent_date
            + relativedelta(days=63 - 1, hour=23, minute=59, second=59, microsecond=999999),
            "1070": consent_date
            + relativedelta(days=105 - 1, hour=23, minute=59, second=59, microsecond=999999),
            "1112": consent_date
            + relativedelta(days=161 - 1, hour=23, minute=59, second=59, microsecond=999999),
            "1168": consent_date
            + relativedelta(days=224 - 1, hour=23, minute=59, second=59, microsecond=999999),
        }

        visits = self.get_subject_visit().visits.timepoint_dates(dt=consent_date)
        for visit in visits:
            with self.subTest(visit_code=visit.code):
                expected_visit_ceiling = expected_visit_window_ceilings.get(visit.code)
                self.assertEqual(visit.dates.upper, expected_visit_ceiling)

    def test_visit_window_ceilings_against_absolute_dates(self):
        consent_date = datetime(
            year=2022, month=3, day=9, hour=9, minute=25, tzinfo=ZoneInfo("UTC")
        )
        expected_visit_window_ceilings = {
            "1000": consent_date,
            "1003": datetime(year=2022, month=3, day=15, tzinfo=ZoneInfo("UTC")),
            "1009": datetime(year=2022, month=3, day=21, tzinfo=ZoneInfo("UTC")),
            "1014": datetime(year=2022, month=3, day=29, tzinfo=ZoneInfo("UTC")),
            "1028": datetime(year=2022, month=5, day=10, tzinfo=ZoneInfo("UTC")),
            "1070": datetime(year=2022, month=6, day=21, tzinfo=ZoneInfo("UTC")),
            "1112": datetime(year=2022, month=8, day=16, tzinfo=ZoneInfo("UTC")),
            "1168": datetime(year=2022, month=10, day=18, tzinfo=ZoneInfo("UTC")),
        }
        for visit_code in expected_visit_window_ceilings:
            expected_visit_window_ceilings[visit_code] = expected_visit_window_ceilings[
                visit_code
            ].replace(hour=23, minute=59, second=59, microsecond=999999)

        visits = self.get_subject_visit().visits.timepoint_dates(dt=consent_date)
        for visit in visits:
            with self.subTest(visit_code=visit.code):
                expected_visit_ceiling = expected_visit_window_ceilings.get(visit.code)
                self.assertEqual(visit.dates.upper, expected_visit_ceiling)
