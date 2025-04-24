#!/bin/bash

rm -rf error output log plots
rm -rf *.dag.*
rm -rf *.csv


mkdir -p error output log plots

wget -O chicago_community_areas_2025.csv "https://data.cityofchicago.org/api/views/igwz-8jzy/rows.csv?date=20250423&accessType=DOWNLOAD"


ls -1 /staging/groups/stat_dscp/group10/tnp_trip_*.csv > fileInputList
condor_submit_dag complete.dag
