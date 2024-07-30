create view rm488_consented as
(
select
    uuid()                           as `id`,
    now()                            as `created`,
    'effect_reports.rm488_consented' as `report_model`,
    site_id,
    screening_identifier,
    initials
from
    effect_screening_subjectscreening
where
    consented = 1
    );
