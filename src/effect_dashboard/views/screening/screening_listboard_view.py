from edc_listboard.views import ScreeningListboardView as BaseScreeningListboardView


class ScreeningListboardView(BaseScreeningListboardView):
    listboard_model = "effect_screening.subjectscreening"
