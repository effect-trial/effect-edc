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
    - add new fields: 'any_signs_symptoms', 'signs_and_symptoms_gte_g3', 'headache_duration_microseconds'
    - add N/A options for if no/unknown answer to 'any_signs_symptoms'
    - add validation

0.1.1
-----
- add migrations

0.1.0
-----
- initial release
