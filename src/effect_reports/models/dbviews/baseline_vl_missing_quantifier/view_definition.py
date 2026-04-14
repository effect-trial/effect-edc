from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    subquery = """select v.subject_identifier,
                         crf.id as crf_id,
                         crf.site_id,
                         v.visit_code,
                         v.visit_code_sequence,
                         CONCAT_WS(".", v.visit_code, v.visit_code_sequence) as visit_code_str,
                         crf.has_viral_load_result,
                         crf.viral_load_result,
                         crf.viral_load_quantifier,
                         crf.viral_load_date,
                         crf.viral_load_date_estimated,
                         crf.user_created,
                         crf.user_modified,
                         crf.modified,
                         '' as label,
                  from effect_subject_arvhistory as crf
                           left join effect_subject_subjectvisit as v
                                     on v.id = crf.subject_visit_id
                  where crf.viral_load_quantifier is null
                     or crf.viral_load_quantifier==''"""

    sql_view = SqlViewGenerator(
        report_model="effect_reports.baselinevlmissingquantifier",
        ordering=["site_id", "subject_identifier", "visit_code", "visit_code_sequence"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
