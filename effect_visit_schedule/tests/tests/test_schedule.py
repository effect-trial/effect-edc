from django.test import TestCase

from effect_visit_schedule.visit_schedules import schedule, visit_schedule


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
            "chemistry_lft",
            "chemistry_rft",
            "csf_culture",
            "fbc",
            "sputum",
            "tissue_biopsy",
        ]
        expected = {
            "1000": [
                "blood_culture",
                "csf_culture",
                "fbc",
                "sputum",
                "tissue_biopsy",
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
                self.assertEqual(
                    expected.get(visit_code),
                    actual,
                    msg=f"see requisitions for visit {visit_code}",
                )
                actual = [requisition.name for requisition in visit.requisitions_prn]
                actual.sort()
                self.assertEqual(
                    prn, actual, msg=f"see PRN requisitions for visit {visit_code}"
                )

    def test_crfs(self):
        prn = [
            "effect_subject.bloodculture",
            "effect_subject.bloodresultsfbc",
            "effect_subject.bloodresultslft",
            "effect_subject.bloodresultsrft",
            "effect_subject.healtheconomics",
            "effect_subject.histopathology",
            "effect_subject.lpcsf",
            "effect_subject.microbiology",
        ]
        expected = {
            "1000": [
                "effect_subject.followup",
                "effect_subject.signsandsymptoms",
                "effect_subject.mentalstatus",
                "effect_subject.vitalsigns",
                "effect_subject.diagnoses",
                "effect_subject.chestxray",
                "effect_subject.arvtreatment",
                "effect_subject.patienttreatment",
                "effect_subject.bloodresultsfbc",
                "effect_subject.lpcsf",
                "effect_subject.microbiology",
                "effect_subject.bloodculture",
                "effect_subject.histopathology",
                "effect_subject.healtheconomics",
                "effect_subject.clinicalnote",
            ],
            "1003": [
                "effect_subject.followup",
                "effect_subject.adherence",
            ],
            "1009": [
                "effect_subject.followup",
                "effect_subject.adherence",
            ],
            "1014": [
                "effect_subject.followup",
                "effect_subject.adherence",
            ],
            "1028": [
                "effect_subject.followup",
                "effect_subject.adherence",
            ],
            "1070": [
                "effect_subject.followup",
                "effect_subject.adherence",
            ],
            "1112": [
                "effect_subject.followup",
                "effect_subject.adherence",
            ],
            "1168": [
                "effect_subject.followup",
                "effect_subject.adherence",
                "effect_subject.healtheconomics",
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
                self.assertEqual(
                    prn, actual, msg=f"see PRN CRFs for visit {visit_code}"
                )
