from edc_model.models import BaseUuidModel
from edc_screening.model_mixins import ScreeningModelMixin
from edc_screening.screening_identifier import (
    ScreeningIdentifier as BaseScreeningIdentifier,
)


class SubjectScreeningModelError(Exception):
    pass


class ScreeningIdentifier(BaseScreeningIdentifier):

    template = "S{random_string}"


class SubjectScreening(
    ScreeningModelMixin,
    BaseUuidModel,
):

    identifier_cls = ScreeningIdentifier

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
