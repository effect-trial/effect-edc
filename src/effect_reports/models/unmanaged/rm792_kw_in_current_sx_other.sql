create view rm792_kw_in_current_sx_other as
(
select
    uuid()                                   as `id`,
    now()                                    as `created`,
    'effect_reports.rm792kwincurrentsxother' as `report_model`,
    `sv`.`site_id`,
    `sv`.`subject_identifier`,
    `sv`.`visit_code`,
    `sv`.`visit_code_sequence`,
    `crf`.`id`                               as crf_id,
    `crf`.`current_sx_other`,
    `crf`.`user_created`,
    `crf`.`user_modified`,
    `crf`.`modified`
from
    `effect_subject_signsandsymptoms` as `crf`
        left join `effect_subject_subjectvisit` as `sv` on `crf`.`subject_visit_id` = `sv`.`id`
where
    `current_sx_other` like '%abdom%'
    or `current_sx_other` like '%appet%'
    or `current_sx_other` like '%back%'
    or `current_sx_other` like '%behav%'
    or `current_sx_other` like '%conf%'
    or `current_sx_other` like '%consti%'
    or `current_sx_other` like '%diar%'
    or `current_sx_other` like '%disten%'
    or `current_sx_other` like '%diz%'
    or `current_sx_other` like '%dry%'
    or `current_sx_other` like '%fatig%'
    or `current_sx_other` like '%insom%'
    or `current_sx_other` like '%itch%'
    or `current_sx_other` like '%mala%'
    or `current_sx_other` like '%nasal%'
    or `current_sx_other` like '%neuro%'
    or `current_sx_other` like '%nose%'
    or `current_sx_other` like '%palp%'
    or `current_sx_other` like '%pleur%'
    or `current_sx_other` like '%rash%'
    or `current_sx_other` like '%rhin%'
    or `current_sx_other` like '%run%'
    or `current_sx_other` like '%urin%'
    or `current_sx_other` like '%weak%'
order by
    `site_id`, `subject_identifier`, `visit_code`, `visit_code_sequence`
    );
