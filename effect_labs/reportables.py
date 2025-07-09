from edc_constants.constants import FEMALE, MALE
from edc_reportable import PERCENT, Formula
from edc_reportable.adult_age_options import adult_age_options
from edc_reportable.data import africa, daids_july_2017

grading_data = {}
grading_data.update(**daids_july_2017.dummies)
grading_data.update(**daids_july_2017.chemistries)
grading_data.update(**daids_july_2017.hematology)

collection_name = "effect"
normal_data = africa.normal_data


normal_data.update(
    {
        "neutrophil_diff": [
            Formula(
                "0<=x<=99999",
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "lymphocyte": [
            Formula(
                "0<=x<=99999",
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "lymphocyte_diff": [
            Formula(
                "0<=x<=99999",
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "csf_wbc": [
            Formula(
                "0<=x<=99999",
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "csf_glucose": [
            Formula(
                "0<=x<=99999",
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "csf_protein": [
            Formula(
                "0<=x<=99999",
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "csf_crag": [
            Formula(
                "0<=x<=99999",
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "csf_crag_lfa": [
            Formula(
                "0<=x<=99999",
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
    }
)

grading_data.update(
    {
        "neutrophil_diff": [
            Formula(
                "x<0",
                grade=0,
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "lymphocyte": [
            Formula(
                "x<0",
                grade=0,
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "lymphocyte_diff": [
            Formula(
                "x<0",
                grade=0,
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "csf_wbc": [
            Formula(
                "x<0",
                grade=0,
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "csf_glucose": [
            Formula(
                "x<0",
                grade=0,
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "csf_protein": [
            Formula(
                "x<0",
                grade=0,
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "csf_crag": [
            Formula(
                "x<0",
                grade=0,
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "csf_crag_lfa": [
            Formula(
                "x<0",
                grade=0,
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
        "proteinuria": [
            Formula(
                "x<0",
                grade=0,
                units=PERCENT,
                gender=[MALE, FEMALE],
                **adult_age_options,
            )
        ],
    }
)


reportable_grades = [3, 4]
reportable_grades_exceptions = {}
