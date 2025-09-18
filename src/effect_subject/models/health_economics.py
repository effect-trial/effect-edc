from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from ..choices import EDUCATIONAL_ATTAINMENT_CHOICES
from ..model_mixins import CrfModelMixin


class HealthEconomics(CrfModelMixin, edc_models.BaseUuidModel):
    occupation = models.CharField(
        verbose_name="What is your occupation/profession?",
        max_length=50,
        blank=False,
        default="",
    )

    education_years = models.IntegerField(
        verbose_name="How many years of education did you compete?",
        validators=[MinValueValidator(0), MaxValueValidator(30)],
        null=True,
        blank=False,
    )

    educational_attainment = models.CharField(  # noqa: DJ001
        verbose_name="What is your highest education certificate?",
        max_length=50,
        choices=EDUCATIONAL_ATTAINMENT_CHOICES,
        blank=False,
        null=True,
    )

    primary_school = models.CharField(  # noqa: DJ001
        verbose_name="Did you go to primary/elementary school?",
        max_length=15,
        choices=YES_NO,
        blank=False,
        null=True,
    )

    primary_school_years = models.IntegerField(
        verbose_name="If YES, for how many years?",
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        null=True,
        blank=True,
    )

    secondary_school = models.CharField(  # noqa: DJ001
        verbose_name="Did you go to secondary school?",
        max_length=15,
        choices=YES_NO,
        blank=False,
        null=True,
    )

    secondary_school_years = models.IntegerField(
        verbose_name="If YES, for how many years?",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )

    higher_education = models.CharField(  # noqa: DJ001
        verbose_name="Did you go to higher education?",
        max_length=15,
        choices=YES_NO,
        null=True,
    )

    higher_education_years = models.IntegerField(
        verbose_name="If YES, for how many years?",
        validators=[MinValueValidator(0), MaxValueValidator(15)],
        null=True,
        blank=True,
    )

    welfare = models.CharField(  # noqa: DJ001
        verbose_name="Do you receive any welfare or social service support?",
        max_length=15,
        choices=YES_NO,
        blank=False,
        null=True,
    )

    monthly_household_income = models.IntegerField(
        verbose_name="What is the total income in your household per month?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
        null=True,
        blank=False,
    )

    highest_earner = models.CharField(  # noqa: DJ001
        verbose_name="Are you the person who earns the highest income in your household?",
        max_length=15,
        choices=YES_NO,
        blank=False,
        null=True,
    )

    profession_highest_earner = models.CharField(
        verbose_name=(
            "If NO, what is the profession of the person who earns the highest income?"
        ),
        max_length=50,
        blank=True,
        default="",
    )

    food_month = models.IntegerField(
        verbose_name="How much does your household spend on food in a month?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
        null=True,
        blank=False,
    )

    accommodation_month = models.IntegerField(
        verbose_name="How much does your household spend on rent (or house loan/mortgage) "
        "and utilities in a month?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
        null=True,
        blank=False,
    )

    large_items_year = models.IntegerField(
        verbose_name="How much have you spent on large items (e.g., furniture, electrical "
        "items, cars) in the last year?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
        null=True,
        blank=False,
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Health Economics"
        verbose_name_plural = "Health Economics"
