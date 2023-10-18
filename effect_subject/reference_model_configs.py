from edc_reference import ReferenceModelConfig, site_reference_configs

site_reference_configs.register_from_visit_schedule(
    visit_models={"edc_appointment.appointment": "effect_subject.subjectvisit"}
)

# Register main Adherence model (only accessed via proxy models)
site_reference_configs.register(
    reference_config=ReferenceModelConfig(
        "effect_subject.adherence",
        fields=["report_datetime"],
    )
)

# Register main Study Medication model (only accessed via proxy models)
site_reference_configs.register(
    reference_config=ReferenceModelConfig(
        "effect_subject.studymedication",
        fields=["report_datetime"],
    )
)

site_reference_configs.add_fields_to_config(
    name="effect_subject.signsandsymptoms",
    fields=["xray_performed", "lp_performed", "urinary_lam_performed"],
)

site_reference_configs.add_fields_to_config(
    name="effect_subject.subjectvisit",
    fields=["assessment_type"],
)
