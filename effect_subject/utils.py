from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

if TYPE_CHECKING:
    from .models import SubjectVisit


def get_weight_in_kgs(subject_visit: SubjectVisit | None) -> Decimal | None:
    """Returns the weight in kg or None.

    Tries current visit. If not found looks for a recording from a
    previous visit.
    """
    weight_in_kgs = None
    try:
        obj = django_apps.get_model("effect_subject.vitalsigns").objects.get(
            subject_visit=subject_visit
        )
    except ObjectDoesNotExist:
        if obj := (
            django_apps.get_model("effect_subject.vitalsigns")
            .objects.filter(
                subject_visit__subject_identifier=subject_visit,
                report_datetime__lt=subject_visit.report_datetime,
            )
            .order_by("report_datetime")
            .last()
        ):
            weight_in_kgs = obj.weight
    else:
        weight_in_kgs = obj.weight

    return weight_in_kgs
