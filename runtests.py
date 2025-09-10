#!/usr/bin/env python

from edc_test_settings.func_main import func_main2

if __name__ == "__main__":

    func_main2(
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
