from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_UNKNOWN
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models

from ..constants import IF_NO_SPECIFY_REASON
from ..model_mixins import CrfModelMixin


class Adherence(CrfModelMixin, edc_models.BaseUuidModel):
    proxy_null_default_options = dict(
        null=False,
        default=NOT_APPLICABLE,
    )

    proxy_yes_no_options = dict(
        max_length=15,
        choices=YES_NO,
        **proxy_null_default_options,
    )

    adherence_counselling = models.CharField(
        verbose_name="Has appropriate adherence counselling been given as per the trial SOP?",
        **proxy_yes_no_options,
    )
    adherence_counselling_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    diary_issued = models.CharField(
        verbose_name="Was an adherence diary issued to the patient?",
        **proxy_yes_no_options,
    )
    diary_issued_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    any_doses_missed = models.CharField(
        verbose_name="Have any doses been missed since the last visit?",
        max_length=15,
        choices=YES_NO_UNKNOWN,
        **proxy_null_default_options,
    )

    fluconazole_doses_missed = models.IntegerField(
        verbose_name="If 'Yes', number of doses missed: FLU",
        help_text="This should be measured in single doses (1 dose per day)",
        validators=[MinValueValidator(1), MaxValueValidator(14 * 1)],
        null=True,
        blank=True,
    )

    flucytosine_doses_missed = models.IntegerField(
        verbose_name="If 'Yes', number of doses missed: 5FC",
        help_text="This should be measured in single doses (4 doses per day)",
        validators=[MinValueValidator(1), MaxValueValidator(14 * 4)],
        null=True,
        blank=True,
    )

    pill_count_conducted = models.CharField(
        verbose_name="Was a pill count conducted?",
        **proxy_yes_no_options,
    )

    pill_count_conducted_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    diary_returned = models.CharField(
        verbose_name="Was patient adherence diary received and stored in patient records?",
        **proxy_yes_no_options,
    )

    diary_returned_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    diary_match_pill_count = models.CharField(
        verbose_name="Did the patient adherence diary match the pill count?",
        **proxy_yes_no_options,
    )

    diary_match_pill_count_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    opinion_fluconazole_adherent = models.CharField(
        verbose_name="In the clinician’s opinion, is the patient 90% adherent to Fluconazole?",
        **proxy_yes_no_options,
    )

    opinion_art_adherent = models.CharField(
        verbose_name="In the clinician’s opinion, is the patient 90% adherent to ART?",
        **proxy_yes_no_options,
    )

    adherence_narrative = models.TextField(
        verbose_name="Medication adherence narrative:",
        null=True,
        blank=True,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Adherence"
        verbose_name_plural = "Adherence"
