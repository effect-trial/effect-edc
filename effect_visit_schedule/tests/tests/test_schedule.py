from datetime import datetime
from zoneinfo import ZoneInfo

from django.test import TestCase, tag

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_visit_schedule.visit_schedules import schedule, visit_schedule


@tag("vsched")
class TestVisitSchedule(TestCase):
    def test_visit_schedule_models(self):
        self.assertEqual(visit_schedule.death_report_model, "effect_ae.deathreport")
        self.assertEqual(visit_schedule.offstudy_model, "edc_offstudy.subjectoffstudy")
        self.assertEqual(visit_schedule.locator_model, "edc_locator.subjectlocator")

    def test_schedule_models(self):
        self.assertEqual(schedule.onschedule_model, "effect_prn.onschedule")
        self.assertEqual(schedule.offschedule_model, "effect_prn.endofstudy")
        self.assertEqual(schedule.consent_model, "effect_consent.subjectconsent")
        self.assertEqual(schedule.appointment_model, "edc_appointment.appointment")

    def test_visit_codes(self):
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
        prn = [
            "effect_subject.bloodculture",
            "effect_subject.bloodresultsfbc",
            "effect_subject.bloodresultschem",
            "effect_subject.healtheconomicsevent",
            "effect_subject.histopathology",
            "effect_subject.chestxray",
            "effect_subject.lpcsf",
            "effect_subject.tbdiagnostics",
            "effect_subject.studymedicationfollowup",
        ]
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
                "effect_subject.mentalstatus",
                "effect_subject.signsandsymptoms",
                "effect_subject.diagnoses",
                "effect_subject.chestxray",
                "effect_subject.lpcsf",
                "effect_subject.tbdiagnostics",
                "effect_subject.adherencestagetwo",
            ],
            "1009": [
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
                "effect_subject.mentalstatus",
                "effect_subject.signsandsymptoms",
                "effect_subject.diagnoses",
                "effect_subject.chestxray",
                "effect_subject.lpcsf",
                "effect_subject.tbdiagnostics",
                "effect_subject.adherencestagefour",
            ],
            "1070": [
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
                "effect_subject.mentalstatus",
                "effect_subject.signsandsymptoms",
                "effect_subject.diagnoses",
                "effect_subject.chestxray",
                "effect_subject.lpcsf",
                "effect_subject.tbdiagnostics",
                "effect_subject.adherencestagefour",
            ],
            "1168": [
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
        for visit_code, visit in schedule.visits.items():
            with self.subTest(visit_code=visit_code, visit=visit):
                actual = [crf.model for crf in visit.crfs]
                actual.sort()
                expected.get(visit_code).sort()
                self.assertEqual(
                    expected.get(visit_code),
                    actual,
                    msg=f"see CRFs for visit {visit_code}",
                )

                actual = [crf.model for crf in visit.crfs_prn]
                actual.sort()
                prn.sort()
                self.assertEqual(prn, actual, msg=f"see PRN CRFs for visit {visit_code}")


@tag("vsched")
class TestVisitScheduleDates(EffectTestCaseMixin, TestCase):
    def test_generated_visit_dates_as_expected(self):
        consent_date = datetime(year=2022, month=3, day=10, hour=9, tzinfo=ZoneInfo("UTC"))
        expected = {
            "1000": consent_date,
            "1003": datetime(year=2022, month=3, day=12, hour=9, tzinfo=ZoneInfo("UTC")),
            "1009": datetime(year=2022, month=3, day=18, hour=9, tzinfo=ZoneInfo("UTC")),
            "1014": datetime(year=2022, month=3, day=23, hour=9, tzinfo=ZoneInfo("UTC")),
            "1028": datetime(year=2022, month=4, day=7, hour=9, tzinfo=ZoneInfo("UTC")),
            "1070": datetime(year=2022, month=5, day=19, hour=9, tzinfo=ZoneInfo("UTC")),
            "1112": datetime(year=2022, month=6, day=30, hour=9, tzinfo=ZoneInfo("UTC")),
            "1168": datetime(year=2022, month=8, day=25, hour=9, tzinfo=ZoneInfo("UTC")),
        }

        actual = {
            visit.code: visit_date
            for visit, visit_date in self.get_subject_visit()
            .visits.timepoint_dates(dt=consent_date)
            .items()
        }

        self.assertDictEqual(expected, actual)
