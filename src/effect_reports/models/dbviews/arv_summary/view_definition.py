from edc_qareports.sql_generator import SqlViewGenerator


def get_view_definition() -> dict:
    subquery = """
        select rs.subject_identifier,
        rs.user_created,
        rs.user_modified,
        rs.modified,
        rs.site_id as site_id,
        '' as visit_code,
        0 as visit_code_sequence,
        ''                                                  as label,
        from edc_registration_registeredsubject as rs
        left join effect_prn_arvsummary as crf
        on rs.subject_identifier = crf.subject_identifier
        """

    sql_view = SqlViewGenerator(
        report_model="effect_reports.arvsummaryreport",
        ordering=["subject_identifier"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
