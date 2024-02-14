from typing import Dict

from django.conf import settings
from django.contrib.sites.models import Site
from django.test import TestCase
from edc_refusal.forms import SubjectRefusalForm
from edc_refusal.models import RefusalReasons, SubjectRefusal
from edc_utils.date import get_utcnow

from ..effect_test_case_mixin import EffectTestCaseMixin


class TestSubjectRefusal(EffectTestCaseMixin, TestCase):
    def setUp(self) -> None:
        self.subject_screening = self.get_subject_screening()

    def get_data(self) -> Dict:
        refusal_reason = RefusalReasons.objects.all()[0]
        return {
            "screening_identifier": self.subject_screening.screening_identifier,
            "report_datetime": get_utcnow(),
            "reason": refusal_reason,
            "other_reason": None,
            "comment": None,
            "site": Site.objects.get(id=settings.SITE_ID).id,
        }

    def test_subject_refusal_ok(self):
        form = SubjectRefusalForm(data=self.get_data(), instance=None)
        form.is_valid()
        self.assertEqual(form._errors, {})
        form.save()
        self.assertEqual(SubjectRefusal.objects.all().count(), 1)

    def test_add_subject_refusal_set_subject_screening_refused_true(self):
        self.assertFalse(self.subject_screening.refused)

        form = SubjectRefusalForm(data=self.get_data(), instance=None)
        form.save()
        self.subject_screening.refresh_from_db()
        self.assertTrue(self.subject_screening.refused)

    def test_delete_subject_refusal_sets_subject_screening_refused_false(self):
        self.assertFalse(self.subject_screening.refused)

        form = SubjectRefusalForm(data=self.get_data(), instance=None)
        form.save()
        self.subject_screening.refresh_from_db()
        self.assertTrue(self.subject_screening.refused)

        subject_refusal = SubjectRefusal.objects.get(
            screening_identifier=self.subject_screening.screening_identifier
        )
        subject_refusal.delete()
        self.subject_screening.refresh_from_db()
        self.assertFalse(self.subject_screening.refused)
