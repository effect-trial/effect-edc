from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import TestCase
from edc_appointment.models import Appointment
from edc_constants.constants import (
    IN_PERSON,
    NEG,
    NO,
    NOT_APPLICABLE,
    OTHER,
    TELEPHONE,
    YES,
)
from edc_metadata import KEYED, REQUIRED
from edc_metadata.models import CrfMetadata
from edc_visit_schedule.constants import DAY01, DAY03
from model_bakery import baker

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin

if TYPE_CHECKING:
    from effect_screening.models import SubjectScreening


class TestMetadataRules(EffectTestCaseMixin, TestCase):
    @staticmethod
    def get_metadata_models(subject_visit):
        crf_metadatas = CrfMetadata.objects.filter(
            subject_identifier=subject_visit.subject_identifier,
            visit_code=subject_visit.visit_code,
            visit_code_sequence=subject_visit.visit_code_sequence,
        )
        return [
            obj.model
            for obj in crf_metadatas.filter(entry_status__in=[KEYED, REQUIRED]).order_by(
                "model"
            )
        ]

    def get_subject_screening_with_lp_done(self) -> SubjectScreening:
        subject_screening = self.get_subject_screening()
        subject_screening.lp_done = YES
        subject_screening.lp_date = subject_screening.report_datetime
        subject_screening.lp_declined = NOT_APPLICABLE
        subject_screening.csf_crag_value = NEG
        subject_screening.save()
        self.assertTrue(subject_screening.eligible)
        self.assertEqual(subject_screening.lp_done, YES)
        self.assertEqual(subject_screening.lp_declined, NOT_APPLICABLE)
        return subject_screening

    def get_subject_screening_with_lp_declined(self) -> SubjectScreening:
        subject_screening = self.get_subject_screening()
        subject_screening.lp_done = NO
        subject_screening.lp_date = None
        subject_screening.lp_declined = YES
        subject_screening.csf_crag_value = NOT_APPLICABLE
        subject_screening.save()
        self.assertTrue(subject_screening.eligible)
        self.assertEqual(subject_screening.lp_done, NO)
        self.assertEqual(subject_screening.lp_declined, YES)
        return subject_screening

    def test_investigations_crfs_not_required_if_sisx_not_completed(self):
        subject_visit = self.get_subject_visit(
            # Avoid triggering lpcsf_crf_required metadata rule with screening lp
            subject_screening=self.get_subject_screening_with_lp_declined()
        )

        for obj in Appointment.objects.filter(
            subject_identifier=subject_visit.subject_identifier
        ).order_by("visit_code"):
            with self.subTest(visit_code=obj.visit_code, subject_visit=subject_visit):
                self.assertEqual(subject_visit.visit_code, obj.visit_code)

                models = self.get_metadata_models(subject_visit)
                self.assertNotIn("effect_subject.chestxray", models)
                self.assertNotIn("effect_subject.lpcsf", models)
                self.assertNotIn("effect_subject.tbdiagnostics", models)
            try:
                subject_visit = self.get_next_subject_visit(subject_visit)
            except AttributeError:
                # Hit here after calling get_next_subject_visit() on last visit
                break

    def test_investigations_crfs_not_required_if_sisx_investigations_not_performed(
        self,
    ):
        subject_visit = self.get_subject_visit(
            # Avoid triggering lpcsf_crf_required metadata rule with screening lp
            subject_screening=self.get_subject_screening_with_lp_declined()
        )

        for obj in Appointment.objects.filter(
            subject_identifier=subject_visit.subject_identifier
        ).order_by("visit_code"):
            with self.subTest(visit_code=obj.visit_code, subject_visit=subject_visit):
                self.assertEqual(subject_visit.visit_code, obj.visit_code)

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
            try:
                subject_visit = self.get_next_subject_visit(subject_visit)
            except AttributeError:
                # Hit here after calling get_next_subject_visit() on last visit
                break

    def test_investigations_crfs_not_required_if_sisx_investigations_na(self):
        subject_visit = self.get_subject_visit(
            # Avoid triggering lpcsf_crf_required metadata rule with screening lp
            subject_screening=self.get_subject_screening_with_lp_declined()
        )

        for obj in Appointment.objects.filter(
            subject_identifier=subject_visit.subject_identifier
        ).order_by("visit_code"):
            with self.subTest(visit_code=obj.visit_code, subject_visit=subject_visit):
                self.assertEqual(subject_visit.visit_code, obj.visit_code)

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
            try:
                subject_visit = self.get_next_subject_visit(subject_visit)
            except AttributeError:
                # Hit here after calling get_next_subject_visit() on last visit
                break

    def test_investigations_crfs_required_if_sisx_investigations_performed(self):
        subject_visit = self.get_subject_visit(
            # Avoid triggering lpcsf_crf_required metadata rule with screening lp
            subject_screening=self.get_subject_screening_with_lp_declined()
        )

        for obj in Appointment.objects.filter(
            subject_identifier=subject_visit.subject_identifier
        ).order_by("visit_code"):
            with self.subTest(visit_code=obj.visit_code, subject_visit=subject_visit):
                self.assertEqual(subject_visit.visit_code, obj.visit_code)

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
            try:
                subject_visit = self.get_next_subject_visit(subject_visit)
            except AttributeError:
                # Hit here after calling get_next_subject_visit() on last visit
                break

    def test_lpcsf_crf_required_at_baseline_if_only_screening_lp_performed(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.get_subject_screening_with_lp_done()
        )
        self.assertEqual(subject_visit.visit_code, DAY01)
        self.assertEqual(subject_visit.visit_code_sequence, 0)
        models = self.get_metadata_models(subject_visit)
        self.assertIn("effect_subject.lpcsf", models)

        signs_and_symptoms = baker.make(
            "effect_subject.signsandsymptoms",
            subject_visit=subject_visit,
            lp_performed=NO,
        )
        signs_and_symptoms.save()
        models = self.get_metadata_models(subject_visit)
        self.assertIn("effect_subject.lpcsf", models)

    def test_lpcsf_crf_required_at_baseline_if_scr_lp_declined_but_diagnosis_lp_performed(
        self,
    ):
        subject_visit = self.get_subject_visit(
            subject_screening=self.get_subject_screening_with_lp_declined()
        )
        self.assertEqual(subject_visit.visit_code, DAY01)
        self.assertEqual(subject_visit.visit_code_sequence, 0)
        models = self.get_metadata_models(subject_visit)
        self.assertNotIn("effect_subject.lpcsf", models)

        signs_and_symptoms = baker.make(
            "effect_subject.signsandsymptoms",
            subject_visit=subject_visit,
            lp_performed=YES,
        )
        signs_and_symptoms.save()
        models = self.get_metadata_models(subject_visit)
        self.assertIn("effect_subject.lpcsf", models)

    def test_lpcsf_crf_required_at_baseline_if_screening_and_diagnosis_lp_performed(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.get_subject_screening_with_lp_done()
        )
        self.assertEqual(subject_visit.visit_code, DAY01)
        self.assertEqual(subject_visit.visit_code_sequence, 0)
        models = self.get_metadata_models(subject_visit)
        self.assertIn("effect_subject.lpcsf", models)

        signs_and_symptoms = baker.make(
            "effect_subject.signsandsymptoms",
            subject_visit=subject_visit,
            lp_performed=YES,
        )
        signs_and_symptoms.save()
        models = self.get_metadata_models(subject_visit)
        self.assertIn("effect_subject.lpcsf", models)

    def test_lpcsf_crf_not_required_at_baseline_if_no_lp_performed(self):
        subject_visit = self.get_subject_visit(
            subject_screening=self.get_subject_screening_with_lp_declined()
        )
        self.assertEqual(subject_visit.visit_code, DAY01)
        self.assertEqual(subject_visit.visit_code_sequence, 0)
        models = self.get_metadata_models(subject_visit)
        self.assertNotIn("effect_subject.lpcsf", models)

        signs_and_symptoms = baker.make(
            "effect_subject.signsandsymptoms",
            subject_visit=subject_visit,
            lp_performed=NO,
        )
        signs_and_symptoms.save()
        models = self.get_metadata_models(subject_visit)
        self.assertNotIn("effect_subject.lpcsf", models)

    # Post baseline tests
    def test_lpcsf_crf_not_required_post_baseline_if_only_screening_lp_performed(self):
        subject_screening = self.get_subject_screening_with_lp_done()
        subject_consent = self.get_subject_consent(subject_screening=subject_screening)

        # Baseline
        subject_visit = self.get_subject_visit(
            subject_screening=subject_screening,
            subject_consent=subject_consent,
        )
        self.assertEqual(subject_visit.visit_code, DAY01)
        models = self.get_metadata_models(subject_visit)
        self.assertIn("effect_subject.lpcsf", models)

        # Post baseline
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, DAY03)

        for obj in (
            Appointment.objects.filter(subject_identifier=subject_visit.subject_identifier)
            .exclude(visit_code=DAY01)
            .order_by("visit_code")
        ):
            with self.subTest(visit_code=obj.visit_code, subject_visit=subject_visit):
                self.assertEqual(subject_visit.visit_code, obj.visit_code)

                models = self.get_metadata_models(subject_visit)
                self.assertNotIn("effect_subject.lpcsf", models)

                signs_and_symptoms = baker.make(
                    "effect_subject.signsandsymptoms",
                    subject_visit=subject_visit,
                    lp_performed=NO,
                )
                signs_and_symptoms.save()
                models = self.get_metadata_models(subject_visit)
                self.assertNotIn("effect_subject.lpcsf", models)

                # Test on unscheduled visit
                unscheduled_appt = self.create_unscheduled_appointment(
                    appointment=subject_visit.appointment
                )
                self.assertEqual(unscheduled_appt.visit_code, obj.visit_code)
                self.assertEqual(unscheduled_appt.visit_code_sequence, 1)

                unscheduled_visit = self.get_subject_visit(
                    visit_code=obj.visit_code,
                    visit_code_sequence=1,
                    subject_screening=subject_screening,
                    subject_consent=subject_consent,
                )
                self.assertEqual(unscheduled_visit.visit_code, obj.visit_code)
                self.assertEqual(unscheduled_visit.visit_code_sequence, 1)
                models = self.get_metadata_models(unscheduled_visit)
                self.assertNotIn("effect_subject.lpcsf", models)

                signs_and_symptoms = baker.make(
                    "effect_subject.signsandsymptoms",
                    subject_visit=unscheduled_visit,
                    lp_performed=NO,
                )
                signs_and_symptoms.save()
                models = self.get_metadata_models(unscheduled_visit)
                self.assertNotIn("effect_subject.lpcsf", models)

                try:
                    subject_visit = self.get_next_subject_visit(subject_visit)
                except AttributeError:
                    # Hit here after calling get_next_subject_visit() on last visit
                    break

    def test_lpcsf_crf_required_post_baseline_if_diagnosis_lp_performed(self):
        subject_screening = self.get_subject_screening_with_lp_declined()
        subject_consent = self.get_subject_consent(subject_screening=subject_screening)

        # Baseline
        subject_visit = self.get_subject_visit(
            subject_screening=subject_screening,
            subject_consent=subject_consent,
        )
        self.assertEqual(subject_visit.visit_code, DAY01)
        models = self.get_metadata_models(subject_visit)
        self.assertNotIn("effect_subject.lpcsf", models)

        signs_and_symptoms = baker.make(
            "effect_subject.signsandsymptoms",
            subject_visit=subject_visit,
            lp_performed=NO,
        )
        signs_and_symptoms.save()
        models = self.get_metadata_models(subject_visit)
        self.assertNotIn("effect_subject.lpcsf", models)

        # Post baseline
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, DAY03)

        for obj in (
            Appointment.objects.filter(subject_identifier=subject_visit.subject_identifier)
            .exclude(visit_code=DAY01)
            .order_by("visit_code")
        ):
            self.assertEqual(obj.visit_code, subject_visit.visit_code)
            self.assertEqual(subject_visit.visit_code_sequence, 0)

            with self.subTest(visit_code=obj.visit_code, subject_visit=subject_visit):
                models = self.get_metadata_models(subject_visit)
                self.assertNotIn("effect_subject.lpcsf", models)

                signs_and_symptoms = baker.make(
                    "effect_subject.signsandsymptoms",
                    subject_visit=subject_visit,
                    lp_performed=YES,
                )
                signs_and_symptoms.save()
                models = self.get_metadata_models(subject_visit)
                self.assertIn("effect_subject.lpcsf", models)

                # Test on unscheduled visit
                unscheduled_appt = self.create_unscheduled_appointment(
                    appointment=subject_visit.appointment
                )
                self.assertEqual(unscheduled_appt.visit_code, obj.visit_code)
                self.assertEqual(unscheduled_appt.visit_code_sequence, 1)

                unscheduled_visit = self.get_subject_visit(
                    visit_code=obj.visit_code,
                    visit_code_sequence=1,
                    subject_screening=subject_screening,
                    subject_consent=subject_consent,
                )
                self.assertEqual(unscheduled_visit.visit_code, obj.visit_code)
                self.assertEqual(unscheduled_visit.visit_code_sequence, 1)
                models = self.get_metadata_models(unscheduled_visit)
                self.assertNotIn("effect_subject.lpcsf", models)

                signs_and_symptoms = baker.make(
                    "effect_subject.signsandsymptoms",
                    subject_visit=unscheduled_visit,
                    lp_performed=YES,
                )
                signs_and_symptoms.save()
                models = self.get_metadata_models(unscheduled_visit)
                self.assertIn("effect_subject.lpcsf", models)

            try:
                subject_visit = self.get_next_subject_visit(subject_visit)
            except AttributeError:
                # Hit here after calling get_next_subject_visit() on last visit
                break

    def test_lpcsf_crf_not_required_post_baseline_if_baseline_diag_lp_but_no_further_diag_lp(
        self,
    ):
        # Baseline
        subject_visit = self.get_subject_visit(
            subject_screening=self.get_subject_screening_with_lp_declined()
        )
        self.assertEqual(subject_visit.visit_code, DAY01)
        models = self.get_metadata_models(subject_visit)
        self.assertNotIn("effect_subject.lpcsf", models)

        signs_and_symptoms = baker.make(
            "effect_subject.signsandsymptoms",
            subject_visit=subject_visit,
            lp_performed=YES,
        )
        signs_and_symptoms.save()
        models = self.get_metadata_models(subject_visit)
        self.assertIn("effect_subject.lpcsf", models)

        # Post baseline
        subject_visit = self.get_next_subject_visit(subject_visit)
        self.assertEqual(subject_visit.visit_code, DAY03)

        for obj in (
            Appointment.objects.filter(subject_identifier=subject_visit.subject_identifier)
            .exclude(visit_code=DAY01)
            .order_by("visit_code")
        ):
            self.assertEqual(obj.visit_code, subject_visit.visit_code)
            self.assertEqual(subject_visit.visit_code_sequence, 0)

            with self.subTest(visit_code=obj.visit_code, subject_visit=subject_visit):
                models = self.get_metadata_models(subject_visit)
                self.assertNotIn("effect_subject.lpcsf", models)

                signs_and_symptoms = baker.make(
                    "effect_subject.signsandsymptoms",
                    subject_visit=subject_visit,
                    lp_performed=NO,
                )
                signs_and_symptoms.save()
                models = self.get_metadata_models(subject_visit)
                self.assertNotIn("effect_subject.lpcsf", models)

            try:
                subject_visit = self.get_next_subject_visit(
                    subject_visit,
                    assessment_type=IN_PERSON,
                )
            except AttributeError:
                # Hit here after calling get_next_subject_visit() on last visit
                break

    def test_vitalsigns_crf_always_required_at_baseline(self):
        """In practice, baseline would always be IN_PERSON.

        This test ensures if for any reason that is not the case
        (e.g. the validation enforcing IN_PERSON at baseline is changed)
        that the Vital Signs form is still required.
        """
        for assessment_type in [IN_PERSON, TELEPHONE, OTHER]:
            with self.subTest(assessment_type=assessment_type):
                subject_screening = self.get_subject_screening()
                subject_consent = self.get_subject_consent(subject_screening=subject_screening)

                # Baseline
                subject_visit = self.get_subject_visit(
                    subject_screening=subject_screening,
                    subject_consent=subject_consent,
                    assessment_type=assessment_type,
                )
                self.assertEqual(subject_visit.assessment_type, assessment_type)
                models = self.get_metadata_models(subject_visit)
                # expect vital signs present at baseline, regardless of assessment type
                self.assertIn("effect_subject.vitalsigns", models)

    def test_vitalsigns_crf_required_if_visit_assessment_type_IN_PERSON(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening=subject_screening)

        # Baseline
        subject_visit = self.get_subject_visit(
            subject_screening=subject_screening,
            subject_consent=subject_consent,
            assessment_type=IN_PERSON,
        )
        self.assertEqual(subject_visit.assessment_type, IN_PERSON)
        models = self.get_metadata_models(subject_visit)
        self.assertIn("effect_subject.vitalsigns", models)

        # Post baseline
        subject_visit = self.get_next_subject_visit(subject_visit, assessment_type=IN_PERSON)
        self.assertEqual(subject_visit.visit_code, DAY03)
        self.assertEqual(subject_visit.assessment_type, IN_PERSON)

        for obj in (
            Appointment.objects.filter(subject_identifier=subject_visit.subject_identifier)
            .exclude(visit_code=DAY01)
            .order_by("visit_code")
        ):
            self.assertEqual(obj.visit_code, subject_visit.visit_code)
            self.assertEqual(subject_visit.visit_code_sequence, 0)
            self.assertEqual(subject_visit.assessment_type, IN_PERSON)

            with self.subTest(visit_code=obj.visit_code, subject_visit=subject_visit):
                models = self.get_metadata_models(subject_visit)
                self.assertIn("effect_subject.vitalsigns", models)

                # Test on unscheduled visit
                unscheduled_appt = self.create_unscheduled_appointment(
                    appointment=subject_visit.appointment
                )
                self.assertEqual(unscheduled_appt.visit_code, obj.visit_code)
                self.assertEqual(unscheduled_appt.visit_code_sequence, 1)

                unscheduled_visit = self.get_subject_visit(
                    visit_code=obj.visit_code,
                    visit_code_sequence=1,
                    subject_screening=subject_screening,
                    subject_consent=subject_consent,
                    assessment_type=IN_PERSON,
                )
                self.assertEqual(unscheduled_visit.visit_code, obj.visit_code)
                self.assertEqual(unscheduled_visit.visit_code_sequence, 1)
                self.assertEqual(subject_visit.assessment_type, IN_PERSON)

                models = self.get_metadata_models(unscheduled_visit)
                self.assertIn("effect_subject.vitalsigns", models)

            try:
                subject_visit = self.get_next_subject_visit(
                    subject_visit,
                    assessment_type=IN_PERSON,
                )
            except AttributeError:
                # Hit here after calling get_next_subject_visit() on last visit
                break

    def test_vitalsigns_crf_not_required_if_visit_assessment_type_TELEPHONE(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening=subject_screening)

        # Baseline
        subject_visit = self.get_subject_visit(
            subject_screening=subject_screening,
            subject_consent=subject_consent,
            assessment_type=IN_PERSON,  # expect IN_PERSON at baseline
        )
        self.assertEqual(subject_visit.assessment_type, IN_PERSON)
        models = self.get_metadata_models(subject_visit)
        # expect vital signs present at baseline, regardless of assessment type
        self.assertIn("effect_subject.vitalsigns", models)

        # Post baseline
        subject_visit = self.get_next_subject_visit(subject_visit, assessment_type=TELEPHONE)
        self.assertEqual(subject_visit.visit_code, DAY03)
        self.assertEqual(subject_visit.assessment_type, TELEPHONE)

        for obj in (
            Appointment.objects.filter(subject_identifier=subject_visit.subject_identifier)
            .exclude(visit_code=DAY01)
            .order_by("visit_code")
        ):
            self.assertEqual(obj.visit_code, subject_visit.visit_code)
            self.assertEqual(subject_visit.visit_code_sequence, 0)
            self.assertEqual(subject_visit.assessment_type, TELEPHONE)

            with self.subTest(visit_code=obj.visit_code, subject_visit=subject_visit):
                models = self.get_metadata_models(subject_visit)
                self.assertNotIn("effect_subject.vitalsigns", models)

                # Test on unscheduled visit
                unscheduled_appt = self.create_unscheduled_appointment(
                    appointment=subject_visit.appointment
                )
                self.assertEqual(unscheduled_appt.visit_code, obj.visit_code)
                self.assertEqual(unscheduled_appt.visit_code_sequence, 1)

                unscheduled_visit = self.get_subject_visit(
                    visit_code=obj.visit_code,
                    visit_code_sequence=1,
                    subject_screening=subject_screening,
                    subject_consent=subject_consent,
                    assessment_type=TELEPHONE,
                )
                self.assertEqual(unscheduled_visit.visit_code, obj.visit_code)
                self.assertEqual(unscheduled_visit.visit_code_sequence, 1)
                self.assertEqual(subject_visit.assessment_type, TELEPHONE)

                models = self.get_metadata_models(unscheduled_visit)
                self.assertNotIn("effect_subject.vitalsigns", models)

            try:
                subject_visit = self.get_next_subject_visit(
                    subject_visit,
                    assessment_type=TELEPHONE,
                )
            except AttributeError:
                # Hit here after calling get_next_subject_visit() on last visit
                break

    def test_vitalsigns_crf_not_required_if_visit_assessment_type_OTHER(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening=subject_screening)

        # Baseline
        subject_visit = self.get_subject_visit(
            subject_screening=subject_screening,
            subject_consent=subject_consent,
            assessment_type=OTHER,  # expect OTHER at baseline
        )
        self.assertEqual(subject_visit.assessment_type, OTHER)
        models = self.get_metadata_models(subject_visit)
        # expect vital signs present at baseline, regardless of assessment type
        self.assertIn("effect_subject.vitalsigns", models)

        # Post baseline
        subject_visit = self.get_next_subject_visit(subject_visit, assessment_type=OTHER)
        self.assertEqual(subject_visit.visit_code, DAY03)
        self.assertEqual(subject_visit.assessment_type, OTHER)

        for obj in (
            Appointment.objects.filter(subject_identifier=subject_visit.subject_identifier)
            .exclude(visit_code=DAY01)
            .order_by("visit_code")
        ):
            self.assertEqual(obj.visit_code, subject_visit.visit_code)
            self.assertEqual(subject_visit.visit_code_sequence, 0)
            self.assertEqual(subject_visit.assessment_type, OTHER)

            with self.subTest(visit_code=obj.visit_code, subject_visit=subject_visit):
                models = self.get_metadata_models(subject_visit)
                self.assertNotIn("effect_subject.vitalsigns", models)

                # Test on unscheduled visit
                unscheduled_appt = self.create_unscheduled_appointment(
                    appointment=subject_visit.appointment
                )
                self.assertEqual(unscheduled_appt.visit_code, obj.visit_code)
                self.assertEqual(unscheduled_appt.visit_code_sequence, 1)

                unscheduled_visit = self.get_subject_visit(
                    visit_code=obj.visit_code,
                    visit_code_sequence=1,
                    subject_screening=subject_screening,
                    subject_consent=subject_consent,
                    assessment_type=OTHER,
                )
                self.assertEqual(unscheduled_visit.visit_code, obj.visit_code)
                self.assertEqual(unscheduled_visit.visit_code_sequence, 1)
                self.assertEqual(subject_visit.assessment_type, OTHER)

                models = self.get_metadata_models(unscheduled_visit)
                self.assertNotIn("effect_subject.vitalsigns", models)

            try:
                subject_visit = self.get_next_subject_visit(
                    subject_visit,
                    assessment_type=OTHER,
                )
            except AttributeError:
                # Hit here after calling get_next_subject_visit() on last visit
                break
