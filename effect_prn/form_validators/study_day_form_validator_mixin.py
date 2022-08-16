from datetime import date
from typing import Any, Optional
from zoneinfo import ZoneInfo

from django import forms
from django.apps import apps as django_apps
from django.conf import settings
from edc_form_validators.base_form_validator import INVALID_ERROR
from edc_utils import convert_php_dateformat


class StudyDayFormValidatorMixin:
    def validate_study_day_with_datetime(
        self: Any,
        subject_identifier: Optional[str] = None,
        study_day: Optional[int] = None,
        compare_date: Optional[date] = None,
        study_day_field: Optional[str] = None,
    ) -> None:
        """Raises an exception if study day does not match
        calculation UTCz.

        Note: study-day is 1-based.
        """
        if study_day is not None and compare_date is not None:
            try:
                compare_date = compare_date.date()  # noqa
            except AttributeError:
                pass
            subject_identifier = (
                subject_identifier
                or self.cleaned_data.get("subject_identifier")
                or self.instance.subject_identifier
            )
            if not subject_identifier:
                raise ValueError(f"Subject identifier cannot be None. See {repr(self)}")
            registered_subject_model_cls = django_apps.get_model(
                "edc_registration.registeredsubject"
            )
            randomization_datetime = registered_subject_model_cls.objects.get(
                subject_identifier=subject_identifier
            ).randomization_datetime
            days_on_study = (compare_date - randomization_datetime.date()).days
            if study_day - 1 != days_on_study:
                randomization_datetime.astimezone(ZoneInfo(settings.TIME_ZONE))
                formatted_date = randomization_datetime.astimezone(
                    ZoneInfo(settings.TIME_ZONE)
                ).strftime(convert_php_dateformat(settings.DATETIME_FORMAT))
                message = {
                    study_day_field: (
                        f"Invalid. Expected {days_on_study + 1}. "
                        f"Subject was registered on {formatted_date}"
                    )
                }
                self._errors.update(message)
                self._error_codes.append(INVALID_ERROR)
                raise forms.ValidationError(message, code=INVALID_ERROR)
