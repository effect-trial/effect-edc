from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_model.models import date_not_future

from effect_lists.models import ArvRegimens

from ..model_mixins import CrfModelMixin


class ArvHistory(CrfModelMixin, edc_models.BaseUuidModel):

    taking_arv_at_crag = models.CharField(
        verbose_name="Was the patient taking ART at time of CrAg test?",
        max_length=5,
        choices=YES_NO,
    )

    ever_taken_arv = models.CharField(
        verbose_name="If NO, has the patient ever been on ART prior to CrAg test?",
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    initial_arv_date = models.DateField(
        verbose_name=mark_safe(
            "If YES, when did the patient <u>start</u> ART for the first time."
        ),
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    initial_arv_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If YES, is this ART date estimated?", default=NOT_APPLICABLE
    )

    initial_arv_regimen = models.ManyToManyField(
        ArvRegimens,
        verbose_name=mark_safe(
            "If YES, which drugs were prescribed for their <u>first</u> ART regimen?"
        ),
        related_name="initial_arv",
    )

    initial_arv_regimen_other = edc_models.OtherCharField()

    has_switched_regimen = models.CharField(
        verbose_name="Has the patient ever switched ART regimen?",
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    current_arv_date = models.DateField(
        verbose_name=mark_safe(
            "If YES, when was their <u>current or most recent</u> "
            "ART regimen started?"
        ),
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    current_arv_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If YES, is this ART date estimated?", default=NOT_APPLICABLE
    )

    current_arv_regimen = models.ManyToManyField(
        ArvRegimens,
        verbose_name="If YES, what is their current or most recent ART regimen?",
        related_name="current_arv",
    )

    current_arv_regimen_other = edc_models.OtherCharField()

    current_arv_is_defaulted = models.CharField(
        verbose_name=mark_safe(
            "Has the patient <u>now</u> defaulted from their ART regimen?"
        ),
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="'DEFAULTED' means no ART for at least one month.",
    )

    current_arv_defaulted_date = models.DateField(
        verbose_name=mark_safe(
            "If the patient has DEFAULTED, on what date did they default "
            "from their <u>most recent</u> ART regimen?"
        ),
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    current_arv_defaulted_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="If DEFAULTED, is this date estimated?", default=NOT_APPLICABLE
    )

    current_arv_is_adherent = models.CharField(
        verbose_name=mark_safe(
            "If the patient is currently on ART, are they ADHERENT to "
            "their <u>current</u> ART regimen?"
        ),
        max_length=5,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
    )

    current_arv_tablets_missed = models.IntegerField(
        verbose_name="If not ADHERENT, how many doses missed in the last month?",
        validators=[MinValueValidator(0), MaxValueValidator(31)],
        null=True,
        blank=True,
    )

    last_viral_load = models.DecimalField(
        verbose_name="Last Viral Load, if known?",
        decimal_places=3,
        max_digits=10,
        null=True,
        blank=True,
        help_text="copies/mL",
    )

    viral_load_date = models.DateField(
        verbose_name="Viral Load date",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    vl_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="Is the subject's Viral Load date estimated?",
        default=NOT_APPLICABLE,
    )

    last_cd4 = models.IntegerField(
        verbose_name="Last CD4, if known?",
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        null=True,
        blank=True,
        help_text=mark_safe("acceptable units are mm<sup>3</sup>"),
    )

    cd4_date = models.DateField(
        verbose_name="CD4 date", validators=[date_not_future], null=True, blank=True
    )

    cd4_date_estimated = edc_models.IsDateEstimatedFieldNa(
        verbose_name="Is the subject's CD4 date estimated?", default=NOT_APPLICABLE
    )

    class Meta(CrfModelMixin.Meta):
        verbose_name = "ARV History"
        verbose_name_plural = "ARV History"
