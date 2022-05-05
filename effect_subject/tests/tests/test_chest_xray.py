# from django.db.models import Q
# from django.test import TestCase, tag
# from edc_constants.choices import YES_NO_NA
# from edc_constants.constants import NO, NORMAL, OTHER, YES
# from edc_constants.utils import get_display
# from model_bakery import baker
#
# from effect_lists.models import XRayResults
# from effect_screening.tests.effect_test_case_mixin import EffectTestCaseMixin
# from effect_subject.forms.chest_xray_form import ChestXrayForm, ChestXrayFormValidator
#
#
# @tag("xr")
# class TestChestXray(EffectTestCaseMixin, TestCase):
#     def setUp(self):
#         super().setUp()
#         self.subject_visit = self.get_subject_visit()
#
#     def test_ok(self):
#         subject_visit = self.subject_visit
#         obj = baker.make_recipe("effect_subject.chestxray", subject_visit=subject_visit)
#         form = ChestXrayForm(instance=obj)
#         form.is_valid()
#
#
# @tag("xr")
# class TestChestXrayFormValidation(EffectTestCaseMixin, TestCase):
#
#     form_validator_default_form_cls = ChestXrayFormValidator
#
#     def setUp(self):
#         super().setUp()
#         self.subject_visit = self.get_subject_visit()
#
#     def set_sisx_xray_performed(self, xray_performed: str):
#         if hasattr(self.subject_visit, "signsandsymptoms"):
#             self.subject_visit.signsandsymptoms.xray_performed = xray_performed
#         else:
#             self.subject_visit.signsandsymptoms = baker.make_recipe(
#                 "effect_subject.signsandsymptoms",
#                 subject_visit=self.subject_visit,
#                 xray_performed=xray_performed,
#             )
#
#     def get_valid_no_chest_xray_data(self):
#         return {
#             "subject_visit": self.subject_visit,
#             "appointment": self.subject_visit.appointment,
#             "report_datetime": self.subject_visit.report_datetime,
#             "chest_xray": NO,
#             "chest_xray_date": "",
#             "chest_xray_results": XRayResults.objects.none(),
#             "chest_xray_results_other": "",
#         }
#
#     def get_valid_chest_xray_data(self):
#         return {
#             "subject_visit": self.subject_visit,
#             "appointment": self.subject_visit.appointment,
#             "report_datetime": self.subject_visit.report_datetime,
#             "chest_xray": YES,
#             "chest_xray_date": self.get_utcnow_as_date(),
#             "chest_xray_results": XRayResults.objects.filter(name=NORMAL),
#             "chest_xray_results_other": "",
#         }
#
#     def test_valid_no_chest_xray_data_ok(self):
#         cleaned_data = self.get_valid_no_chest_xray_data()
#         self.assertFormValidatorNoError(
#             form_validator=self.validate_form_validator(cleaned_data)
#         )
#
#     def test_valid_chest_xray_data_ok(self):
#         cleaned_data = self.get_valid_chest_xray_data()
#         self.assertFormValidatorNoError(
#             form_validator=self.validate_form_validator(cleaned_data)
#         )
#
#     def test_valid_no_chest_xray_data_ok_with_corresponding_sisx_answer(self):
#         cleaned_data = self.get_valid_no_chest_xray_data()
#         self.set_sisx_xray_performed(xray_performed=NO)
#         cleaned_data.update(subject_visit=self.subject_visit)
#         self.assertFormValidatorNoError(
#             form_validator=self.validate_form_validator(cleaned_data)
#         )
#
#     def test_valid_chest_xray_data_ok_with_corresponding_sisx_answer(self):
#         cleaned_data = self.get_valid_chest_xray_data()
#         self.set_sisx_xray_performed(xray_performed=YES)
#         cleaned_data.update(subject_visit=self.subject_visit)
#         self.assertFormValidatorNoError(
#             form_validator=self.validate_form_validator(cleaned_data)
#         )
#
#     def test_chest_xray_yes_raises_if_sisx_xray_performed_not_yes(self):
#         for sisx_xray_performed_choice in [ch[0] for ch in YES_NO_NA if ch[0] != YES]:
#             with self.subTest(sisx_xray_performed=sisx_xray_performed_choice):
#                 cleaned_data = self.get_valid_chest_xray_data()
#                 self.set_sisx_xray_performed(xray_performed=sisx_xray_performed_choice)
#                 cleaned_data.update(subject_visit=self.subject_visit)
#                 self.assertFormValidatorError(
#                     field="chest_xray",
#                     expected_msg=(
#                         "Invalid. Previous answer for 'Was an X-ray performed?' "
#                         "in 'Signs and Symptoms' "
#                         f"was '{get_display(YES_NO_NA, sisx_xray_performed_choice)}'."
#                     ),
#                     form_validator=self.validate_form_validator(cleaned_data),
#                 )
#
#     def test_chest_xray_no_raises_if_sisx_xray_performed_not_no(self):
#         for sisx_xray_performed_choice in [ch[0] for ch in YES_NO_NA if ch[0] != NO]:
#             with self.subTest(sisx_xray_performed=sisx_xray_performed_choice):
#                 cleaned_data = self.get_valid_no_chest_xray_data()
#                 self.set_sisx_xray_performed(xray_performed=sisx_xray_performed_choice)
#                 cleaned_data.update(subject_visit=self.subject_visit)
#                 self.assertFormValidatorError(
#                     field="chest_xray",
#                     expected_msg=(
#                         "Invalid. Previous answer for 'Was an X-ray performed?' "
#                         "in 'Signs and Symptoms' "
#                         f"was '{get_display(YES_NO_NA, sisx_xray_performed_choice)}'."
#                     ),
#                     form_validator=self.validate_form_validator(cleaned_data),
#                 )
#
#     def test_chest_xray_no_does_not_require_date(self):
#         cleaned_data = self.get_valid_no_chest_xray_data()
#         cleaned_data.update(chest_xray_date=self.get_utcnow_as_date())
#         self.assertFormValidatorError(
#             field="chest_xray_date",
#             expected_msg="This field is not required.",
#             form_validator=self.validate_form_validator(cleaned_data),
#         )
#
#     def test_chest_xray_yes_requires_date(self):
#         cleaned_data = self.get_valid_chest_xray_data()
#         cleaned_data.update(chest_xray_date="")
#         self.assertFormValidatorError(
#             field="chest_xray_date",
#             expected_msg="This field is required.",
#             form_validator=self.validate_form_validator(cleaned_data),
#         )
#
#     def test_chest_xray_no_does_not_require_result(self):
#         cleaned_data = self.get_valid_no_chest_xray_data()
#         cleaned_data.update(
#             chest_xray_results=XRayResults.objects.filter(name="consolidation")
#         )
#         self.assertFormValidatorError(
#             field="chest_xray_results",
#             expected_msg="This field is not required",
#             form_validator=self.validate_form_validator(cleaned_data),
#         )
#
#     def test_chest_xray_yes_requires_result(self):
#         cleaned_data = self.get_valid_chest_xray_data()
#         cleaned_data.update(chest_xray_results=XRayResults.objects.none())
#         self.assertFormValidatorError(
#             field="chest_xray_results",
#             expected_msg="This field is required",
#             form_validator=self.validate_form_validator(cleaned_data),
#         )
#
#     def test_cannot_have_other_results_with_normal(self):
#         cleaned_data = self.get_valid_chest_xray_data()
#         cleaned_data.update(
#             chest_xray_results=XRayResults.objects.filter(
#                 Q(name=NORMAL) | Q(name="consolidation") | Q(name="infiltrates")
#             )
#         )
#         self.assertFormValidatorError(
#             field="chest_xray_results",
#             expected_msg=(
#                 "Invalid combination. 'Normal' may not be combined with other selections"
#             ),
#             form_validator=self.validate_form_validator(cleaned_data),
#         )
#
#         cleaned_data.update(
#             chest_xray_results=XRayResults.objects.filter(
#                 Q(name="consolidation") | Q(name="infiltrates")
#             )
#         )
#         self.assertFormValidatorNoError(
#             form_validator=self.validate_form_validator(cleaned_data)
#         )
#
#         cleaned_data.update(
#             chest_xray_results=XRayResults.objects.filter(Q(name=NORMAL))
#         )
#         self.assertFormValidatorNoError(
#             form_validator=self.validate_form_validator(cleaned_data)
#         )
#
#     def test_chest_xray_results_other_required_if_result_is_other(self):
#         cleaned_data = self.get_valid_chest_xray_data()
#         cleaned_data.update(chest_xray_results=XRayResults.objects.filter(name=OTHER))
#         self.assertFormValidatorError(
#             field="chest_xray_results_other",
#             expected_msg="This field is required.",
#             form_validator=self.validate_form_validator(cleaned_data),
#         )
#
#         cleaned_data.update(chest_xray_results_other="Some other result")
#         self.assertFormValidatorNoError(
#             form_validator=self.validate_form_validator(cleaned_data),
#         )
#
#     def test_chest_xray_results_other_not_required_if_result_is_not_other(self):
#         cleaned_data = self.get_valid_chest_xray_data()
#         cleaned_data.update(chest_xray_results_other="Some other result")
#         self.assertFormValidatorError(
#             field="chest_xray_results_other",
#             expected_msg="This field is not required.",
#             form_validator=self.validate_form_validator(cleaned_data),
#         )
