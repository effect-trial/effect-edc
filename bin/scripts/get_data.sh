#!/bin/bash

# usage: sh get_data.sh tanzania,south_africa
echo "Path: /export"

cd ~/app || exit

# *** Includes edc_randomization ***
#python manage.py export_models --country=$1 -f stata -p ~/export/ --use-simple-filename -a effect_screening,effect_subject,effect_prn,effect_ae,effect_consent,>
#    -f csv \
#    -f stata \
#    -a edc_randomization


#    -f stata \
#    -f csv \

python manage.py export_models \
    --country=$1 \
    -f stata \
    -p ~/export/ \
    --use-simple-filename \
    -a effect_ae,effect_consent,effect_lists,effect_prn,effect_screening,effect_subject,edc_appointment,edc_data_manager,edc_metadata,edc_registration,edc_visit > $2

echo "Done"
