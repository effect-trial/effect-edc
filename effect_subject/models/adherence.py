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

    any_fluconazole_doses_missed = models.CharField(
        verbose_name="Have any Fluconazole doses been missed since the last visit?",
        max_length=15,
        choices=YES_NO_UNKNOWN,
        **proxy_null_default_options,
    )

    fluconazole_doses_missed = models.IntegerField(
        verbose_name="If 'Yes', number of Fluconazole doses missed since last visit:",
        help_text="This should be measured in single doses (1 dose per day)",
        validators=[MinValueValidator(0), MaxValueValidator(14 * 1)],
        default=0,
    )

    any_flucytosine_doses_missed = models.CharField(
        verbose_name="Have any Flucytosine doses been missed since the last visit?",
        max_length=15,
        choices=YES_NO_UNKNOWN,
        **proxy_null_default_options,
    )

    flucytosine_doses_missed = models.IntegerField(
        verbose_name="If 'Yes', number of Flucytosine doses missed since last visit:",
        help_text="This should be measured in single doses (4 doses per day)",
        validators=[MinValueValidator(0), MaxValueValidator(14 * 4)],
        default=0,
    )

    medication_reconciliation = models.CharField(
        verbose_name="Was a medication reconciliation conducted?",
        **proxy_yes_no_options,
    )

    medication_reconciliation_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    diary_returned = models.CharField(
        verbose_name="Was patient adherence diary received and stored in patient records?",
        **proxy_yes_no_options,
    )

    diary_returned_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    diary_match_medication = models.CharField(
        verbose_name="Did the patient adherence diary match the medication reconciliation?",
        **proxy_yes_no_options,
    )

    diary_match_medication_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    linked_local_clinic = models.CharField(
        verbose_name="Have you linked up with your local clinic?",
        **proxy_yes_no_options,
    )

    linked_local_clinic_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    receiving_fluconazole = models.CharField(
        verbose_name="Are you receiving Fluconazole?",
        **proxy_yes_no_options,
    )

    receiving_fluconazole_reason_no = edc_models.OtherCharField(
        verbose_name=IF_NO_SPECIFY_REASON
    )

    receiving_arv = models.CharField(
        verbose_name="Are you receiving ARVs?",
        **proxy_yes_no_options,
    )

    receiving_arv_reason_no = edc_models.OtherCharField(
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
