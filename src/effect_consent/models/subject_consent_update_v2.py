from django.db import models
from edc_action_item.models import ActionModelMixin
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_sites.model_mixins import SiteModelMixin
from edc_utils import get_utcnow

from ..constants import CONSENT_V2_ACTION
from .special_consent_fields_model_mixin import SpecialConsentFieldsModelMixin


class SubjectConsentUpdateV2(
    UniqueSubjectIdentifierFieldMixin,
    SpecialConsentFieldsModelMixin,
    SiteModelMixin,
    ActionModelMixin,
    BaseUuidModel,
):
    action_name = CONSENT_V2_ACTION

    consent_datetime = models.DateTimeField(
        verbose_name="Consent date and time", default=get_utcnow
    )

    def __str__(self):
        return self.subject_identifier

    class Meta(ActionModelMixin.Meta, BaseUuidModel.Meta):
        verbose_name = "Consent Version 2 (Update)"
        verbose_name_plural = "Consent Version 2 (Update)"
