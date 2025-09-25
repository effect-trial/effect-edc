from edc_qareports.sql_generator import SqlViewGenerator

from ..search_terms import search_terms


def get_view_definition() -> dict:
    subquery = """select
    `v`.`site_id`,
    `v`.`subject_identifier`,
    `v`.`visit_code`,
    `v`.`visit_code_sequence`,
    `crf`.`id`                                    as crf_id,
    `crf`.`current_sx_gte_g3_other`,
    `crf`.`user_created`,
    `crf`.`user_modified`,
    `crf`.`modified`
    from
    `effect_subject_signsandsymptoms` as `crf`
        left join `effect_subject_subjectvisit` as `v` on `crf`.`subject_visit_id` = `v`.`id`
    WHERE `current_sx_gte_g3_other` REGEXP '{}'""".format("|".join(search_terms))

    sql_view = SqlViewGenerator(
        report_model="effect_reports.rm792_kw_in_current_sx_gte_g3_other",
        ordering=["site_id", "subject_identifier", "visit_code", "visit_code_sequence"],
    )
    return {
        "django.db.backends.mysql": sql_view.as_mysql(subquery),
        "django.db.backends.postgresql": sql_view.as_postgres(subquery),
        "django.db.backends.sqlite3": sql_view.as_sqlite(subquery),
    }
