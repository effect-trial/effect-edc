from django.test import TestCase, tag
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_metadata import KEYED, REQUIRED
from edc_metadata.models import CrfMetadata
from model_bakery import baker

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
from effect_visit_schedule.visit_schedules.schedule import visits


@tag("mdr")
class TestMetadataRules(EffectTestCaseMixin, TestCase):

    scheduled_visit_codes = [v.code for v in visits]

    @staticmethod
    def get_metadata_models(subject_visit):
        crf_metadatas = CrfMetadata.objects.filter(
            subject_identifier=subject_visit.subject_identifier,
            visit_code=subject_visit.visit_code,
            visit_code_sequence=subject_visit.visit_code_sequence,
        )
        return [
            obj.model
            for obj in crf_metadatas.filter(
                entry_status__in=[KEYED, REQUIRED]
            ).order_by("model")
        ]

    def test_investigations_crfs_not_required_if_sisx_not_completed(self):
        subject_visit = self.get_subject_visit()
        for visit_code in self.scheduled_visit_codes:
            with self.subTest(visit_code=visit_code):
                # If not baseline visit
                if visit_code != self.scheduled_visit_codes[0]:
                    subject_visit = self.get_next_subject_visit(subject_visit)
                self.assertEqual(subject_visit.appointment.visit_code, visit_code)

                models = self.get_metadata_models(subject_visit)
                self.assertNotIn("effect_subject.chestxray", models)
                self.assertNotIn("effect_subject.lpcsf", models)
                self.assertNotIn("effect_subject.tbdiagnostics", models)

    def test_investigations_crfs_not_required_if_sisx_investigations_not_performed(
        self,
    ):
        subject_visit = self.get_subject_visit()
        for visit_code in self.scheduled_visit_codes:
            with self.subTest(visit_code=visit_code, subject_visit=subject_visit):
                # If not baseline visit
                if visit_code != self.scheduled_visit_codes[0]:
                    subject_visit = self.get_next_subject_visit(subject_visit)
                self.assertEqual(subject_visit.appointment.visit_code, visit_code)

                signs_and_symptoms = baker.make(
                    "effect_subject.signsandsymptoms",
                    subject_visit=subject_visit,
                    xray_performed=NO,
                    lp_performed=NO,
                    urinary_lam_performed=NO,
                )
                signs_and_symptoms.save()
                models = self.get_metadata_models(subject_visit)
                self.assertNotIn("effect_subject.chestxray", models)
                self.assertNotIn("effect_subject.lpcsf", models)
                self.assertNotIn("effect_subject.tbdiagnostics", models)

    def test_investigations_crfs_not_required_if_sisx_investigations_na(self):
        subject_visit = self.get_subject_visit()
        for visit_code in self.scheduled_visit_codes:
            with self.subTest(visit_code=visit_code, subject_visit=subject_visit):
                # If not baseline visit
                if visit_code != self.scheduled_visit_codes[0]:
                    subject_visit = self.get_next_subject_visit(subject_visit)
                self.assertEqual(subject_visit.appointment.visit_code, visit_code)

                signs_and_symptoms = baker.make(
                    "effect_subject.signsandsymptoms",
                    subject_visit=subject_visit,
                    xray_performed=NOT_APPLICABLE,
                    lp_performed=NOT_APPLICABLE,
                    urinary_lam_performed=NOT_APPLICABLE,
                )
                signs_and_symptoms.save()
                models = self.get_metadata_models(subject_visit)
                self.assertNotIn("effect_subject.chestxray", models)
                self.assertNotIn("effect_subject.lpcsf", models)
                self.assertNotIn("effect_subject.tbdiagnostics", models)

    def test_investigations_crfs_required_if_if_sisx_investigations_performed(self):
        subject_visit = self.get_subject_visit()
        for visit_code in self.scheduled_visit_codes:
            with self.subTest(visit_code=visit_code, subject_visit=subject_visit):
                # If not baseline visit
                if visit_code != self.scheduled_visit_codes[0]:
                    subject_visit = self.get_next_subject_visit(subject_visit)
                self.assertEqual(subject_visit.appointment.visit_code, visit_code)

                signs_and_symptoms = baker.make(
                    "effect_subject.signsandsymptoms",
                    subject_visit=subject_visit,
                    xray_performed=NO,
                    lp_performed=NO,
                    urinary_lam_performed=NO,
                )
                signs_and_symptoms.save()

                signs_and_symptoms.xray_performed = YES
                signs_and_symptoms.save()
                models = self.get_metadata_models(subject_visit)
                self.assertIn("effect_subject.chestxray", models)
                self.assertNotIn("effect_subject.lpcsf", models)
                self.assertNotIn("effect_subject.tbdiagnostics", models)

                signs_and_symptoms.lp_performed = YES
                signs_and_symptoms.save()
                models = self.get_metadata_models(subject_visit)
                self.assertIn("effect_subject.chestxray", models)
                self.assertIn("effect_subject.lpcsf", models)
                self.assertNotIn("effect_subject.tbdiagnostics", models)

                signs_and_symptoms.urinary_lam_performed = YES
                signs_and_symptoms.save()
                models = self.get_metadata_models(subject_visit)
                self.assertIn("effect_subject.chestxray", models)
                self.assertIn("effect_subject.lpcsf", models)
                self.assertIn("effect_subject.tbdiagnostics", models)

                signs_and_symptoms.lp_performed = NO
                signs_and_symptoms.save()
                models = self.get_metadata_models(subject_visit)
                self.assertIn("effect_subject.chestxray", models)
                self.assertNotIn("effect_subject.lpcsf", models)
                self.assertIn("effect_subject.tbdiagnostics", models)

                tb_diagnostics = baker.make(
                    "effect_subject.tbdiagnostics",
                    subject_visit=subject_visit,
                )
                tb_diagnostics.save()
                signs_and_symptoms.urinary_lam_performed = NO
                signs_and_symptoms.save()
                models = self.get_metadata_models(subject_visit)
                self.assertIn("effect_subject.chestxray", models)
                self.assertNotIn("effect_subject.lpcsf", models)
                self.assertIn("effect_subject.tbdiagnostics", models)
