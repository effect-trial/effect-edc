import re
from datetime import timedelta
from typing import Optional, Union

from django import forms
from django.db import models
from django.db.models import CharField
from edc_model.utils import InvalidFormat, dh_pattern, raise_on_invalid_field_name


def timedelta_from_duration_dh_field(
    data: Union[dict, models.Model], duration_dh_field: str
) -> Optional[timedelta]:
    """Wrapper function for `duration_dh_to_timedelta` typically called in
    modelform.clean() and model.save().

    Returns timedelta using `duration_dh_to_timedelta` or None.

    Will raise an exception if the string cannot be interpreted.
    """
    duration_timedelta = None
    is_form_data = False
    raise_on_invalid_field_name(data, duration_dh_field)
    try:
        duration_dh_str = data.get(duration_dh_field)
    except AttributeError:
        duration_dh_str = getattr(data, duration_dh_field, None)
    else:
        is_form_data = True

    if duration_dh_str:
        try:
            duration_timedelta = duration_dh_to_timedelta(duration_text=duration_dh_str)
        except InvalidFormat as e:
            if is_form_data:
                raise forms.ValidationError({duration_dh_field: str(e)})
            raise
    return duration_timedelta


def duration_dh_to_timedelta(duration_text: Union[str, CharField]) -> timedelta:
    """Returns timedelta from a well-formatted string
    (specified in days and/or hours).

    Will raise an exception if the string cannot be interpreted.
    """
    duration_text = duration_text.replace(" ", "")
    if not re.match(dh_pattern, duration_text):
        raise InvalidFormat(
            "Expected format is `DDdHHh`, `DDd` or `HHh`. "
            "For example 1d23h, 15d9h ... or 20d, or 5h ..."
            f"Got {duration_text}"
        )
    days = 0
    hours = 0
    if "d" in duration_text:
        days_str, remaining = duration_text.split("d")
        days = int(days_str)
        if remaining and "h" in remaining:
            hours = int(remaining.split("h")[0])
    else:
        hours_str = duration_text.split("h")[0]
        hours = int(hours_str)
    return timedelta(days=days, hours=hours)
