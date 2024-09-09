from datetime import datetime
from unittest import skip
from zoneinfo import ZoneInfo

import time_machine
from django.test import TestCase
from edc_utils import get_utcnow
from model_bakery import baker

from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin


class TestSubjectConsent(EffectTestCaseMixin, TestCase):
    @time_machine.travel(datetime(2024, 4, 22, 13, 59, tzinfo=ZoneInfo("UTC")))
    def test_v1(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        self.assertIsNotNone(subject_consent.subject_identifier)

    @skip
    @time_machine.travel(datetime(2024, 4, 1, 8, 00, tzinfo=ZoneInfo("UTC")))
    def test_v1_to_v2(self):
        traveller = time_machine.travel(datetime(2024, 1, 1, 8, 00, tzinfo=ZoneInfo("UTC")))
        traveller.start()
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        self.assertIsNotNone(subject_consent.subject_identifier)
        self.assertEqual(subject_consent.version, "1")
        # check resave
        subject_consent.save()
        traveller.stop()
        traveller = time_machine.travel(datetime(2024, 2, 10, 8, 00, tzinfo=ZoneInfo("UTC")))
        traveller.start()
        subject_consent = baker.make_recipe(
            "effect_consent.subjectconsent",
            user_created="erikvw",
            user_modified="erikvw",
            screening_identifier=subject_consent.screening_identifier,
            initials=subject_consent.initials,
            gender=subject_consent.gender,
            dob=subject_consent.dob,
            site=subject_consent.site,
            consent_datetime=get_utcnow(),
            subject_identifier=subject_consent.subject_identifier,
            first_name=subject_consent.first_name,
            last_name=subject_consent.last_name,
        )
        self.assertEqual(subject_consent.version, "2")

    @time_machine.travel(datetime(2024, 4, 22, 14, 00, tzinfo=ZoneInfo("UTC")))
    def test_v2(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        self.assertIsNotNone(subject_consent.subject_identifier)
        self.assertEqual(subject_consent.version, "2")
