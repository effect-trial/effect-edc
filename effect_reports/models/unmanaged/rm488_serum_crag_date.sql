create view rm488_serum_crag_date as
(
select
#      *,
    uuid()                                                        as `id`,
    now()                                                         as `created`,
    'effect_reports.rm488_serum_crag_date'                        as `report_model`,
    site_id,
    screening_identifier,
    initials,
    age_in_years,
    gender,
    subject_identifier,
    cast(eligibility_datetime as date)                            as eligibility_date,
    serum_crag_date,
    datediff(serum_crag_date, cast(eligibility_datetime as date)) as days_difference,
#     confirmed_serum_crag_date,
    user_created,
    user_modified
-- , created, modified
from
    effect_screening_subjectscreening
where
    consented = 1
    );
