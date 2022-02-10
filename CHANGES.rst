Changes
=======

[unreleased]
------------
- changes to Follow-up (formerly Clinical Assessment) form:
    - rename/standardise 'Clinical Assessment' to be 'Follow-up' throughout
    - add survival status help text, for 'Deceased' and 'Alive, but unwell' choices
    - modify adherence_counselling to only be applicable if not 'Deceased'
- changes to Signs and Symptoms form:
    - reorder fields based on feedback
    - convert headache_duration to edc_models.DurationDHField
    - use _sx in field names to be consistent ('current_sx', cm_sx')
    - add new model fields: 'any_sx', 'current_sx_other', 'current_sx_gte_g3', 'current_sx_gte_g3_other', 'headache_duration_microseconds', 'cm_sx_lp_done' , 'cm_sx_bloods_taken', 'cm_sx_bloods_taken_other', 'cm_sx_patient_admitted'
    - add N/A options for if no/unknown answer to 'any_sx'
    - add validation
- fix server error when trying to save “mental status” form

0.1.1
-----
- add migrations

0.1.0
-----
- initial release
