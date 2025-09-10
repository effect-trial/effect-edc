from edc_lab import ProcessingProfile, urine, wb
from edc_lab.aliquot_types import csf, tissue_biopsy

fbc_processing = ProcessingProfile(name="FBC", aliquot_type=wb)

chemistry_processing = ProcessingProfile(name="Chem", aliquot_type=wb)

lp_processing = ProcessingProfile(name="LPE", aliquot_type=csf)

csf_culture_processing = ProcessingProfile(name="csf_culture", aliquot_type=csf)

tissue_biopsy_processing = ProcessingProfile(name="TBY", aliquot_type=tissue_biopsy)

blood_culture_processing = ProcessingProfile(name="BLE", aliquot_type=wb)


urinalysis_processing = ProcessingProfile(name="urinalysis", aliquot_type=urine)
