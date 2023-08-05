from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from effect_lists.models import ArvRegimens

from ..model_mixins import CrfModelMixin


class ArvTreatment(CrfModelMixin, edc_models.BaseUuidModel):
    on_arv_regimen = models.CharField(
        verbose_name="Is the participant currently on an ART regimen?",
        max_length=15,
        choices=YES_NO,
        help_text="If ART regimen is on hold, answer YES and clarify below",
    )

    adherent = models.CharField(
        verbose_name=(
            "If YES, on an ART regimen, has the participant adhered to this ART regimen?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="In the opinion of the clinician, is the participant at least 90% adherent",
    )

    # TODO: what do they want to know here?
    arv_regimen_stopped = models.CharField(
        verbose_name="Has ART been held/stopped this clinical episode?",
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    arv_regimen_stopped_date = models.DateField(
        verbose_name="Date held or stopped?",
        null=True,
        blank=True,
    )

    arv_regimen_changed = models.CharField(
        # TODO: determine and display date of last study assessment
        verbose_name=(
            "Has the participant's ART regimen changed since the last study assessment"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=(
            "Also applies if ART started/re-started since enrolment, including at this visit."
        ),
    )

    arv_regimen_start_date = models.DateField(
        # TODO: ???Is this:
        #  Start date of most recent ART regimen?
        #  Start date of new ART regimen?
        # TODO: null = True??
        verbose_name="Start date of the changed ART regimen?",
        null=True,
        blank=True,
    )

    # TODO: Clarify when this question is required (d1, d14),
    #  and/or in response to “decision made re ART?” e.g. stopped, continued etc
    # TODO: null = True??
    # TODO: this should be validated against any previous report, if changed or not.
    arv_regimen = models.ForeignKey(
        ArvRegimens,
        on_delete=models.PROTECT,
        verbose_name="Current ART regimen?",
        null=True,
        blank=True,
        help_text="Required if on an ART regimen",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "ARV Treatment"
        verbose_name_plural = "ARV Treatment"
