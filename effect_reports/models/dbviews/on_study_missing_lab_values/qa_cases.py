from edc_lab_panel.panels import sputum_panel
from edc_qareports.sql_generator import CrfCase, RequisitionCase

from effect_labs.panels import chemistry_panel, csf_culture_panel, fbc_panel

qa_cases = []
for label_lower, panel, id_field in [
    ("effect_subject.bloodresultschem", chemistry_panel, None),
    ("effect_subject.lpcsf", csf_culture_panel, "csf_requisition_id"),
    ("effect_subject.bloodresultsfbc", fbc_panel, None),
    ("effect_subject.tbdiagnostics", sputum_panel, "sputum_requisition_id"),
]:
    qa_cases.append(
        RequisitionCase(
            label=f"{panel.abbreviation.upper()} requisitioned but not entered",
            dbtable=label_lower.replace(".", "_"),
            label_lower=label_lower,
            panel=panel.name,
            requisition_id_field=id_field,
        )
    )

for label_lower, panel in [
    ("effect_subject.bloodresultschem", chemistry_panel),
    ("effect_subject.bloodresultsfbc", fbc_panel),
]:
    for utest_id in panel.utest_ids:
        try:
            utest_id, _ = utest_id
        except ValueError:
            pass
        qa_cases.append(
            CrfCase(
                label=f"{panel.abbreviation.upper()}: missing {utest_id} value/units",
                dbtable=label_lower.replace(".", "_"),
                label_lower=label_lower,
                where=f"crf.{utest_id}_value is null or crf.{utest_id}_units is null",
            )
        )
