from edc_qareports.modeladmin_mixins import NoteStatusListFilter

from effect_reports.choices import NOTE_STATUSES


class SerumCragDateNoteStatusListFilter(NoteStatusListFilter):
    title = "Serum CrAg Date Status"
    parameter_name = "serum_crag_date_note_status"

    note_model_cls = None
    note_model_status_choices = NOTE_STATUSES
