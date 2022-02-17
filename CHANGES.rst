Changes
=======

[unreleased]
------------
- changes to Follow-up (formerly Clinical Assessment) form:
    - rename/standardise 'Clinical Assessment' to be 'Follow-up' throughout
    - add "Other" choice/"Other, please specify..." field to Q3 (Was this a telephone follow up or an in person visit?)
    - add survival status help text, for 'Deceased' and 'Alive, but unwell' choices
    - modify adherence_counselling to only be applicable if not 'Deceased'
    - add AE_INITIAL_ACTION action item if yes answer to 'hospitalized'
- changes to Signs and Symptoms form:
    - reorder fields based on feedback
    - convert headache_duration to edc_models.DurationDHField
    - use _sx in field names to be consistent ('current_sx', cm_sx')
    - add new model fields: 'any_sx', 'current_sx_other', 'current_sx_gte_g3', 'current_sx_gte_g3_other', 'headache_duration_microseconds', 'cm_sx_lp_done' , 'cm_sx_bloods_taken', 'cm_sx_bloods_taken_other', 'cm_sx_patient_admitted'
    - add N/A options for if no/unknown answer to 'any_sx'
    - add validation
    - add AE_INITIAL_ACTION action item if yes answer to any of: 'reportable_as_ae', 'patient_admitted', or 'cm_sx_patient_admitted'
    - merge in Neurological form fields
- changes to Mental Status form:
    - expand Modified Rankin Score choices to include 0 and 6, and add descriptions
- remove:
    - Neurological Symptoms form
    - FocalNeurologicDeficits list model
- fix server error when trying to save “mental status” form

0.1.1
-----
- add migrations

0.1.0
-----
- initial release
