Changes
=======

[unreleased]
------------
- rename Microbiology CRF to TB Diagnostics
- changes to Consent form:
    - remove "Guardian name" field (#346)
- changes to Screening:
    - move "willing to participate?" and "capacity to provide informed consent?" towards bottom of form (#339, #340)
    - remove all "Not answered" responses (#341, #342)
    - validate/prevent saving if CD4 count not < 100 (#345)
    - update verbose_name to ‘Is the patient CONFIRMED HIV sero-positive’
    - Serum CrAg
        - validate/prevent saving if serum CrAg result not positive (#341)
        - remove IND as option for CrAg results
        - validate/prevent saving if serum CrAg date not within last 14 days (#344)
    - change to 'Was CM confirmed in CSF by any other method? etc' and add list of methods
    - explicitly ask about/exclude protocol listed clinical symptoms/signs of symptomatic meningitis (#343)
      (i.e. a progressively severe headache, a headache and marked nuchal rigidity,
      a headache and vomiting, seizures, a Glasgow Coma Scale (GCS) score of <15)
    - separate pregnancy / breastfeeding questions to be like ambition, add preg date
- changes to Follow-up (formerly Clinical Assessment) form:
    - rename/standardise 'Clinical Assessment' to be 'Follow-up' throughout
    - add "Other" choice/"Other, please specify..." field to Q3 (Was this a telephone follow up or an in person visit?)
    - add survival status help text, for 'Deceased' and 'Alive, but unwell' choices
    - modify adherence_counselling to only be applicable if not 'Deceased'
    - add AE_INITIAL_ACTION action item if yes answer to 'hospitalized'
    - validate 'assessment_type' and 'info_source' against 'info_source' answer provided on Subject Visit CRF
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
    - make 'reportable_as_ae' and 'patient_admitted' not applicable at baseline
- changes to AE Initial Form:
    - add new model fields: 'fluconazole_relation', 'flucytosine_relation', 'patient_admitted', 'date_admitted', 'inpatient_status' and 'date_discharged'
    - added 'Hospitalization' section to form/admin
    - reordered 'Cause and relationship to study' form/admin section
- rename Study Treatment form to Patient Treatment
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
