from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.constants import INCOMPLETE_APPT
from edc_constants.constants import NO, NOT_APPLICABLE, YES
from edc_metadata import KEYED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_utils import get_utcnow
from model_bakery import baker

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin


@tag("mdr")
class TestMetadataRules(EffectTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.baseline_datetime = get_utcnow() - relativedelta(months=1)

        self.subject_screening = self.get_subject_screening(
            report_datetime=self.baseline_datetime
        )
        self.subject_consent = self.get_subject_consent(
            subject_screening=self.subject_screening,
            consent_datetime=self.baseline_datetime,
        )

        self.subject_visit_baseline = self.get_subject_visit(
            subject_screening=self.subject_screening,
            subject_consent=self.subject_consent,
        )

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

    def test_investigations_not_performed_do_not_require_crfs(self):
        subject_visit_baseline = self.subject_visit_baseline

        signs_and_symptoms = baker.make(
            "effect_subject.signsandsymptoms",
            subject_visit=subject_visit_baseline,
            report_datetime=self.baseline_datetime,
            xray_performed=NO,
            lp_performed=NO,
            urinary_lam_performed=NO,
        )
        signs_and_symptoms.save()

        subject_visit_baseline.appointment.appt_status = INCOMPLETE_APPT
        subject_visit_baseline.appointment.save()
        subject_visit_baseline.appointment.refresh_from_db()
        subject_visit_baseline.refresh_from_db()

        models = self.get_metadata_models(subject_visit_baseline)
        self.assertNotIn("effect_subject.chestxray", models)
        self.assertNotIn("effect_subject.lpcsf", models)
        self.assertNotIn("effect_subject.tbdiagnostics", models)

    def test_investigations_na_do_not_require_crfs(self):
        subject_visit_baseline = self.subject_visit_baseline

        signs_and_symptoms = baker.make(
            "effect_subject.signsandsymptoms",
            subject_visit=subject_visit_baseline,
            report_datetime=self.baseline_datetime,
            xray_performed=NOT_APPLICABLE,
            lp_performed=NOT_APPLICABLE,
            urinary_lam_performed=NOT_APPLICABLE,
        )
        signs_and_symptoms.save()

        subject_visit_baseline.appointment.appt_status = INCOMPLETE_APPT
        subject_visit_baseline.appointment.save()
        subject_visit_baseline.appointment.refresh_from_db()
        subject_visit_baseline.refresh_from_db()

        models = self.get_metadata_models(subject_visit_baseline)
        self.assertNotIn("effect_subject.chestxray", models)
        self.assertNotIn("effect_subject.lpcsf", models)
        self.assertNotIn("effect_subject.tbdiagnostics", models)

    def test_investigations_performed_do_require_crfs(self):
        subject_visit_baseline = self.subject_visit_baseline

        signs_and_symptoms = baker.make(
            "effect_subject.signsandsymptoms",
            subject_visit=subject_visit_baseline,
            report_datetime=self.baseline_datetime,
            xray_performed=NO,
            lp_performed=NO,
            urinary_lam_performed=NO,
        )
        signs_and_symptoms.save()

        subject_visit_baseline.appointment.appt_status = INCOMPLETE_APPT
        subject_visit_baseline.appointment.save()
        subject_visit_baseline.appointment.refresh_from_db()
        subject_visit_baseline.refresh_from_db()

        models = self.get_metadata_models(subject_visit_baseline)
        self.assertNotIn("effect_subject.chestxray", models)
        self.assertNotIn("effect_subject.lpcsf", models)
        self.assertNotIn("effect_subject.tbdiagnostics", models)

        signs_and_symptoms.xray_performed = YES
        signs_and_symptoms.save()
        models = self.get_metadata_models(subject_visit_baseline)
        self.assertIn("effect_subject.chestxray", models)
        self.assertNotIn("effect_subject.lpcsf", models)
        self.assertNotIn("effect_subject.tbdiagnostics", models)

        signs_and_symptoms.lp_performed = YES
        signs_and_symptoms.save()
        models = self.get_metadata_models(subject_visit_baseline)
        self.assertIn("effect_subject.chestxray", models)
        self.assertIn("effect_subject.lpcsf", models)
        self.assertNotIn("effect_subject.tbdiagnostics", models)

        signs_and_symptoms.urinary_lam_performed = YES
        signs_and_symptoms.save()
        models = self.get_metadata_models(subject_visit_baseline)
        self.assertIn("effect_subject.chestxray", models)
        self.assertIn("effect_subject.lpcsf", models)
        self.assertIn("effect_subject.tbdiagnostics", models)

        signs_and_symptoms.lp_performed = NO
        signs_and_symptoms.save()
        models = self.get_metadata_models(subject_visit_baseline)
        self.assertIn("effect_subject.chestxray", models)
        self.assertNotIn("effect_subject.lpcsf", models)
        self.assertIn("effect_subject.tbdiagnostics", models)

        tb_diagnostics = baker.make(
            "effect_subject.tbdiagnostics",
            subject_visit=subject_visit_baseline,
            report_datetime=self.baseline_datetime,
        )
        tb_diagnostics.save()
        signs_and_symptoms.urinary_lam_performed = NO
        signs_and_symptoms.save()
        models = self.get_metadata_models(subject_visit_baseline)
        self.assertIn("effect_subject.chestxray", models)
        self.assertNotIn("effect_subject.lpcsf", models)
        self.assertIn("effect_subject.tbdiagnostics", models)
