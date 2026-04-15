from clinicedc_constants import NULL_STRING
from django.db import models
from edc_action_item.models import ActionItem, ActionModelMixin
from edc_constants.choices import NOT_APPLICABLE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_model.models import BaseUuidModel
from edc_protocol_incident.constants import PROTOCOL_DEVIATION_VIOLATION_ACTION
from edc_protocol_incident.model_mixins import ProtocolDeviationViolationModelMixin
from edc_sites.model_mixins import SiteModelMixin

from effect_lists.models import MissedDoseResponsibility

from ..choices import (
    ACTION_REQUIRED,
    MISSED_DOSE_CONDITIONS,
    PROTOCOL_VIOLATION,
)


class ProtocolDeviationViolation(
    ProtocolDeviationViolationModelMixin,
    NonUniqueSubjectIdentifierFieldMixin,
    SiteModelMixin,
    ActionModelMixin,
    BaseUuidModel,
):
    action_name = PROTOCOL_DEVIATION_VIOLATION_ACTION

    action_item = models.ForeignKey(
        ActionItem,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="effect_prn_action_item",
    )

    violation_type = models.CharField(
        verbose_name="Type of violation",
        max_length=75,
        choices=PROTOCOL_VIOLATION,
        default=NOT_APPLICABLE,
    )

    violation_type_other = models.CharField(
        default="",
        blank=True,
        verbose_name="If other, please specify",
        max_length=75,
    )

    missed_dose_conditions = models.CharField(
        verbose_name="Which conditions apply?",
        max_length=50,
        choices=MISSED_DOSE_CONDITIONS,
        default=NOT_APPLICABLE,
    )

    missed_dose_count_summary = models.TextField(
        verbose_name="How many / of what / when?",
        default=NULL_STRING,
        blank=True,
    )

    missed_dose_responsibility = models.ManyToManyField(
        MissedDoseResponsibility,
        verbose_name="Who is primarily responsible?",
        blank=True,
    )

    missed_dose_reason = models.TextField(
        verbose_name="Reasons given by ppts for missed induction doses",
        default=NULL_STRING,
        blank=True,
    )

    action_required_old = models.CharField(max_length=45, choices=ACTION_REQUIRED, default="")

    def natural_key(self):
        return (self.action_identifier,)

    class Meta(ProtocolDeviationViolationModelMixin.Meta, BaseUuidModel.Meta):
        pass
