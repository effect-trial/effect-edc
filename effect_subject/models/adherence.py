from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from ..constants import IF_NO_SPECIFY_REASON
from ..model_mixins import CrfModelMixin


class Adherence(CrfModelMixin, edc_models.BaseUuidModel):

    adherence_counselling = models.CharField(
        verbose_name="Has appropriate adherence counselling been given as per the trial SOP?",
        max_length=15,
        choices=YES_NO,
        null=False,
        default=NOT_APPLICABLE,
    )
    adherence_counselling_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    diary_issued = models.CharField(
        verbose_name="Was an adherence diary issued to the participant?",
        max_length=15,
        choices=YES_NO,
        null=False,
        default=NOT_APPLICABLE,
    )
    diary_issued_reason_no = edc_models.OtherCharField(verbose_name=IF_NO_SPECIFY_REASON)

    flucon_doses_missed = models.CharField(
        verbose_name="Have any Fluconazole doses been missed since the last visit?",
        max_length=15,
        choices=YES_NO_UNKNOWN,
        null=False,
        default=NOT_APPLICABLE,
    )

    flucon_doses_missed_number = models.IntegerField(
        verbose_name="If YES, number of Fluconazole doses missed since last visit:",
        help_text="This should be measured in single doses (1 dose per day)",
        validators=[MinValueValidator(0), MaxValueValidator(14 * 1)],
        default=0,
    )

    flucyt_doses_missed = models.CharField(
        verbose_name="Have any Flucytosine doses been missed since the last visit?",
        max_length=15,
        choices=YES_NO_UNKNOWN,
        null=False,
        default=NOT_APPLICABLE,
    )

    flucyt_doses_missed_number = models.IntegerField(
        verbose_name="If YES, number of Flucytosine doses missed since last visit:",
        help_text="This should be measured in single doses (4 doses per day)",
        validators=[MinValueValidator(0), MaxValueValidator(14 * 4)],
        default=0,
    )

    medication_reconciliation = models.CharField(
        verbose_name="Was a medication reconciliation conducted?",
        max_length=15,
        choices=YES_NO,
        null=False,
        default=NOT_APPLICABLE,
    )

    medication_reconciliation_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    diary_returned = models.CharField(
        verbose_name=(
            "Was participant adherence diary received and stored in participant records?"
        ),
        max_length=15,
        choices=YES_NO,
        null=False,
        default=NOT_APPLICABLE,
    )

    diary_returned_reason_no = edc_models.OtherCharField(verbose_name=IF_NO_SPECIFY_REASON)

    diary_match_medication = models.CharField(
        verbose_name=(
            "Did the participant adherence diary match the medication reconciliation?"
        ),
        max_length=15,
        choices=YES_NO,
        null=False,
        default=NOT_APPLICABLE,
    )

    diary_match_medication_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    linked_local_clinic = models.CharField(
        verbose_name="Has the participant linked up with their local clinic?",
        max_length=15,
        choices=YES_NO,
        null=False,
        default=NOT_APPLICABLE,
    )

    linked_local_clinic_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    on_flucon = models.CharField(
        verbose_name="Is the participant receiving Fluconazole?",
        max_length=15,
        choices=YES_NO,
        null=False,
        default=NOT_APPLICABLE,
    )

    on_flucon_reason_no = edc_models.OtherCharField(verbose_name=IF_NO_SPECIFY_REASON)

    on_arv = models.CharField(
        verbose_name="Is the participant receiving ARVs?",
        max_length=15,
        choices=YES_NO,
        null=False,
        default=NOT_APPLICABLE,
    )

    on_arv_reason_no = edc_models.OtherCharField(verbose_name=IF_NO_SPECIFY_REASON)

    opinion_flucon_adherent = models.CharField(
        verbose_name=(
            "In the clinician’s opinion, is the participant 90% adherent to fluconazole?"
        ),
        max_length=15,
        choices=YES_NO,
        null=False,
        default=NOT_APPLICABLE,
    )

    opinion_arv_adherent = models.CharField(
        verbose_name="In the clinician’s opinion, is the participant 90% adherent to ART?",
        max_length=15,
        choices=YES_NO,
        null=False,
        default=NOT_APPLICABLE,
    )

    adherence_narrative = models.TextField(
        verbose_name="Medication adherence narrative:",
        null=True,
        blank=True,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Adherence"
        verbose_name_plural = "Adherence"
