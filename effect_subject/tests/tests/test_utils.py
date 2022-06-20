from datetime import timedelta

from django import forms
from django.test import TestCase, tag
from edc_model import InvalidFieldName, InvalidFormat
from edc_model.models import BaseModel, DurationDHField

from effect_subject.utils import (
    duration_dh_to_timedelta,
    timedelta_from_duration_dh_field,
)


class ModelWithDHDurationValidators(BaseModel):
    duration_dh = DurationDHField(null=True)


@tag("subject_utils")
class TestUtils(TestCase):
    def test_valid_duration_dh_to_timedelta_ok(self):
        test_cases = [
            ("1d", timedelta(days=1, hours=0)),
            ("0d0h", timedelta(days=0, hours=0)),
            ("1h", timedelta(days=0, hours=1)),
            ("00d00h", timedelta(days=0, hours=0)),
            ("000d00h", timedelta(days=0, hours=0)),
            ("0d", timedelta(days=0, hours=0)),
            ("0h", timedelta(days=0, hours=0)),
            ("0d1h", timedelta(days=0, hours=1)),
            ("1d0h", timedelta(days=1, hours=0)),
            ("3d", timedelta(days=3, hours=0)),
            ("10d", timedelta(days=10, hours=0)),
            ("10d0h", timedelta(days=10, hours=0)),
            ("10d9h", timedelta(days=10, hours=9)),
            ("10d10h", timedelta(days=10, hours=10)),
            ("11d", timedelta(days=11, hours=0)),
            ("99d", timedelta(days=99, hours=0)),
            ("100d", timedelta(days=100, hours=0)),
            ("100d0h", timedelta(days=100, hours=0)),
            ("100d9h", timedelta(days=100, hours=9)),
            ("100d23h", timedelta(days=100, hours=23)),
            ("101d", timedelta(days=101, hours=0)),
            ("999d", timedelta(days=999, hours=0)),
            ("4h", timedelta(days=0, hours=4)),
            ("04h", timedelta(days=0, hours=4)),
            ("10h", timedelta(days=0, hours=10)),
            ("11h", timedelta(days=0, hours=11)),
            ("19h", timedelta(days=0, hours=19)),
            ("20h", timedelta(days=0, hours=20)),
            ("21h", timedelta(days=0, hours=21)),
            ("22h", timedelta(days=0, hours=22)),
            ("23h", timedelta(days=0, hours=23)),
        ]
        for duration_dh_str, expected_td in test_cases:
            with self.subTest(duration_dh_str=duration_dh_str, expected_td=expected_td):
                self.assertEqual(duration_dh_to_timedelta(duration_dh_str), expected_td)

    def test_invalid_duration_dh_to_timedelta_raises(self):
        invalid_duration_strings = [
            "0000d",
            "1000d",
            "000h",
            "24h",
            "1d24h",
            "25h",
            "119h",
            "225h",
            "5",
            "15",
            "12345",
            "d",
            "h",
            "x",
            "dh",
            "5d.",
            "5d7",
            "5d10",
            "5d20",
            "5d24h",
            "5d25h",
            "-1d",
            "-1h",
            "-2d3h",
        ]
        for invalid_str in invalid_duration_strings:
            with self.subTest(string=invalid_str):
                with self.assertRaises(InvalidFormat):
                    duration_dh_to_timedelta(invalid_str)

    def test_timedelta_from_duration_dh_field_with_valid_str_ok(self):
        test_cases = [
            ("1d", timedelta(days=1, hours=0)),
            ("0d0h", timedelta(days=0, hours=0)),
            ("1h", timedelta(days=0, hours=1)),
            ("00d00h", timedelta(days=0, hours=0)),
            ("000d00h", timedelta(days=0, hours=0)),
            ("0d", timedelta(days=0, hours=0)),
            ("0h", timedelta(days=0, hours=0)),
            ("0d1h", timedelta(days=0, hours=1)),
            ("1d0h", timedelta(days=1, hours=0)),
            ("3d", timedelta(days=3, hours=0)),
            ("10d", timedelta(days=10, hours=0)),
            ("10d0h", timedelta(days=10, hours=0)),
            ("10d9h", timedelta(days=10, hours=9)),
            ("10d10h", timedelta(days=10, hours=10)),
            ("11d", timedelta(days=11, hours=0)),
            ("99d", timedelta(days=99, hours=0)),
            ("100d", timedelta(days=100, hours=0)),
            ("100d0h", timedelta(days=100, hours=0)),
            ("100d9h", timedelta(days=100, hours=9)),
            ("100d23h", timedelta(days=100, hours=23)),
            ("101d", timedelta(days=101, hours=0)),
            ("999d", timedelta(days=999, hours=0)),
            ("4h", timedelta(days=0, hours=4)),
            ("04h", timedelta(days=0, hours=4)),
            ("10h", timedelta(days=0, hours=10)),
            ("11h", timedelta(days=0, hours=11)),
            ("19h", timedelta(days=0, hours=19)),
            ("20h", timedelta(days=0, hours=20)),
            ("21h", timedelta(days=0, hours=21)),
            ("22h", timedelta(days=0, hours=22)),
            ("23h", timedelta(days=0, hours=23)),
        ]
        for duration_dh_str, expected_td in test_cases:
            with self.subTest(duration_dh_str=duration_dh_str, expected_td=expected_td):
                cleaned_data = {"duration_dh": duration_dh_str}
                td_from_field = timedelta_from_duration_dh_field(
                    data=cleaned_data,
                    duration_dh_field="duration_dh",
                )
                self.assertEqual(td_from_field, expected_td)
                self.assertEqual(
                    td_from_field,
                    duration_dh_to_timedelta(duration_text=duration_dh_str),
                )

    def test_timedelta_from_duration_dh_field_with_invalid_str_raises(self):
        invalid_duration_strings = [
            "0000d",
            "1000d",
            "000h",
            "24h",
            "1d24h",
            "25h",
            "119h",
            "225h",
            "5",
            "15",
            "12345",
            "d",
            "h",
            "x",
            "dh",
            "5d.",
            "5d7",
            "5d10",
            "5d20",
            "5d24h",
            "5d25h",
            "-1d",
            "-1h",
            "-2d3h",
        ]
        for invalid_str in invalid_duration_strings:
            with self.subTest(string=invalid_str):
                cleaned_data = {"duration_dh": invalid_str}
                with self.assertRaises(forms.ValidationError):
                    timedelta_from_duration_dh_field(
                        data=cleaned_data,
                        duration_dh_field="duration_dh",
                    )

    def test_timedelta_from_duration_dh_field_with_missing_field_raises(self):
        cleaned_data = {"duration_dh": "1d"}
        with self.assertRaises(InvalidFieldName):
            timedelta_from_duration_dh_field(
                data=cleaned_data, duration_dh_field="non_existent_field"
            )

    def test_timedelta_from_duration_dh_field_fv_with_valid_data(self):
        obj = ModelWithDHDurationValidators.objects.create(duration_dh="4d")
        td_from_field = timedelta_from_duration_dh_field(
            data=obj, duration_dh_field="duration_dh"
        )
        self.assertEqual(td_from_field, timedelta(days=4))
        self.assertEqual(td_from_field, timedelta(days=4, hours=0))

        obj = ModelWithDHDurationValidators.objects.create(duration_dh="3h")
        td_from_field = timedelta_from_duration_dh_field(
            data=obj, duration_dh_field="duration_dh"
        )
        self.assertEqual(td_from_field, timedelta(hours=3))
        self.assertEqual(td_from_field, timedelta(days=0, hours=3))

        obj = ModelWithDHDurationValidators.objects.create(duration_dh="1d12h")
        td_from_field = timedelta_from_duration_dh_field(
            data=obj, duration_dh_field="duration_dh"
        )
        self.assertEqual(td_from_field, timedelta(days=1, hours=12))

    def test_timedelta_from_duration_dh_field_fv_with_invalid_data_raises(self):
        obj = ModelWithDHDurationValidators.objects.create(duration_dh="1d25h")
        with self.assertRaises(InvalidFormat):
            timedelta_from_duration_dh_field(data=obj, duration_dh_field="duration_dh")

    def test_timedelta_from_duration_dh_field_with_none_returns_none(self):
        obj = ModelWithDHDurationValidators.objects.create(duration_dh=None)
        td_from_field = timedelta_from_duration_dh_field(
            data=obj, duration_dh_field="duration_dh"
        )
        self.assertIsNone(td_from_field)

    def test_timedelta_from_duration_dh_field_with_invalid_filed_name_raises(self):
        obj = ModelWithDHDurationValidators.objects.create(duration_dh="2d")
        for invalid_field_name in ["non_existent_field", "", None]:
            with self.subTest(invalid_field_name=invalid_field_name):
                with self.assertRaises(InvalidFieldName):
                    timedelta_from_duration_dh_field(
                        data=obj, duration_dh_field=invalid_field_name
                    )
