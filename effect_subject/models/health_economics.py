from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class HealthEconomics(CrfModelMixin, edc_models.BaseUuidModel):

    occupation = models.CharField(
        verbose_name="What is your occupation/profession?", max_length=50
    )

    education_years = models.IntegerField(
        verbose_name="How many years of education did you compete?",
        validators=[MinValueValidator(0), MaxValueValidator(30)],
    )

    education_certificate = models.CharField(
        verbose_name="What is your highest education certificate?",
        max_length=50,
    )

    primary_school = models.CharField(
        verbose_name="Did you go to primary/elementary school?",
        max_length=15,
        choices=YES_NO,
    )

    primary_school_years = models.IntegerField(
        verbose_name="If YES, for how many years?",
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        null=True,
        blank=True,
    )

    secondary_school = models.CharField(
        verbose_name="Did you go to secondary school?",
        max_length=15,
        choices=YES_NO,
    )

    secondary_school_years = models.IntegerField(
        verbose_name="If YES, for how many years?",
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True,
    )

    higher_education = models.CharField(
        verbose_name="Did you go to higher education?",
        max_length=15,
        choices=YES_NO,
    )

    higher_education_years = models.IntegerField(
        verbose_name="If YES, for how many years?",
        validators=[MinValueValidator(0), MaxValueValidator(15)],
        null=True,
        blank=True,
    )

    welfare = models.CharField(
        verbose_name="Do you receive any welfare or social service support?",
        max_length=15,
        choices=YES_NO,
    )

    monthly_household_income = models.IntegerField(
        verbose_name="What is the total income in your household per month?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    is_highest_earner = models.CharField(
        verbose_name="Are you the person who earns the highest income in your household?",
        max_length=15,
        choices=YES_NO,
    )

    profession_highest_earner = models.CharField(
        verbose_name="If NO, what is the profession of the person who earns the highest "
        "income?",
        max_length=50,
        null=True,
        blank=True,
    )

    monthly_food = models.IntegerField(
        verbose_name="How much does your household spend on food in a month?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    monthly_accommodation = models.IntegerField(
        verbose_name="How much does your household spend on rent (or house loan/mortgage) "
        "and utilities in a month?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    yearly_large_items = models.IntegerField(
        verbose_name="How much have you spent on large items (e.g., furniture, electrical "
        "items, cars) in the last year?",
        validators=[MinValueValidator(0)],
        help_text="In rands or shillings",
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Health Economics"
        verbose_name_plural = "Health Economics"
