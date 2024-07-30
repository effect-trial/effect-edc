create view rm792_kw_in_current_sx_gte_g3_other as
(
select
    uuid()                                               as `id`,
    now()                                                as `created`,
    'effect_reports.rm792_kw_in_current_sx_gte_g3_other' as `report_model`,
    `sv`.`site_id`,
    `sv`.`subject_identifier`,
    `sv`.`visit_code`,
    `sv`.`visit_code_sequence`,
    `crf`.`current_sx_gte_g3_other`,
    `crf`.`user_created`,
    `crf`.`user_modified`,
    `crf`.`modified`
from
    `effect_subject_signsandsymptoms` as `crf`
        left join `effect_subject_subjectvisit` as `sv` on `crf`.`subject_visit_id` = `sv`.`id`
where
    `current_sx_gte_g3_other` like '%consti%'
    or `current_sx_gte_g3_other` like '%weak%'
    or `current_sx_gte_g3_other` like '%fatig%'
    or `current_sx_gte_g3_other` like '%mala%'
    or `current_sx_gte_g3_other` like '%diar%'
order by
    `site_id`, `subject_identifier`, `visit_code`, `visit_code_sequence`
    );
