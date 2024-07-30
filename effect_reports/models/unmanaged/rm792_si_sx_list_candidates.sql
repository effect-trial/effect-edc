create view rm792_si_sx_list_candidates as
(
select
    uuid()                                       as `id`,
    now()                                        as `created`,
    'effect_reports.rm792_si_sx_list_candidates' as `report_model`,
    sv.site_id,
    crf.current_sx_other

from
    effect_subject_signsandsymptoms as crf
        left join effect_subject_subjectvisit as sv on crf.subject_visit_id = sv.id
where
    current_sx_other like '%abdom%'
    or current_sx_other like '%appet%'
    or current_sx_other like '%back%'
    or current_sx_other like '%conf%'
    or current_sx_other like '%diz%'
    or current_sx_other like '%itchy%'
    or current_sx_other like '%pleur%'
    or current_sx_other like '%rash%'
order by
    current_sx_other);
