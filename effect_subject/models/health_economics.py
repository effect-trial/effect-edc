from django.db import models
from edc_constants.choices import YES_NO
from edc_model import models as edc_models

from ..model_mixins import CrfModelMixin


class HealthEconomics(CrfModelMixin, edc_models.BaseUuidModel):

    occupation = models.CharField(
        verbose_name="What is your occupation/profession?", max_length=45
    )

    education_years = models.IntegerField(
        verbose_name="How many years of education did you compete?"
    )

    highest_education_certificate = models.CharField(
        verbose_name="What is your highest education certificate?",
        max_length=45,
    )

    primary_school = models.CharField(
        verbose_name="Did you go to primary/elementary school?",
        max_length=15,
        choices=YES_NO,
    )

    primary_school_years = models.IntegerField(verbose_name="If YES, for how many years?")

    secondary_school = models.CharField(
        verbose_name="Did you go to secondary school?",
        max_length=15,
        choices=YES_NO,
    )

    secondary_school_years = models.IntegerField(
        verbose_name="If YES, for how many years?",
    )

    higher_education = models.CharField(
        verbose_name="Did you go to higher education?",
        max_length=15,
        choices=YES_NO,
    )

    higher_education_years = models.IntegerField(
        verbose_name="If YES, for how many years?",
    )

    welfare = models.CharField(
        verbose_name="Do you received any welfare?", max_length=15, choices=YES_NO
    )

    monthly_household_income = models.IntegerField(
        verbose_name="What is the total income in your household per month?",
    )

    highest_income_person = models.CharField(
        verbose_name="Are you the person who earns the highest income in your household?",
        max_length=15,
        choices=YES_NO,
    )

    highest_income_person_profession = models.CharField(
        verbose_name="If NO, what is the profession of the person who earns the highest income?",
        max_length=45,
    )

    monthly_household_food_spent = models.IntegerField(
        verbose_name="How much does your household spend on food in a month?",
    )

    monthly_household_rent_spent = models.IntegerField(
        verbose_name="How much does your household spend on rent (or house loan/mortgage) and utilities in a month?",
    )

    yearly_household_large_item_spent = models.IntegerField(
        verbose_name="How much have you spent on large items (e.g., furniture, electrical items, cars) in the last "
        "year? "
    )

    class Meta(CrfModelMixin.Meta, edc_models.BaseUuidModel.Meta):
        verbose_name = "Health Economics"
        verbose_name_plural = "Health Economics"
