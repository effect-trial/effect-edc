#!/usr/bin/env python
from clinicedc_tests.config import func_main

if __name__ == "__main__":
    func_main(
        "tests.test_settings",
        "effect_ae.tests",
        "effect_dashboard.tests",
        "effect_edc.tests",
        "effect_labs.tests",
        "effect_lists.tests",
        "effect_prn.tests",
        "effect_screening.tests",
        "effect_subject.tests",
    )
