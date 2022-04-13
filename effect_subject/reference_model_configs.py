from edc_reference import site_reference_configs

site_reference_configs.register_from_visit_schedule(
    visit_models={"edc_appointment.appointment": "effect_subject.subjectvisit"}
)

site_reference_configs.add_fields_to_config(
    name="effect_subject.signsandsymptoms",
    fields=["xray_performed", "lp_performed", "urinary_lam_performed"],
)
