#!/bin/bash

TOTAL_SPLITS=100

rm -rf /staging/groups/stat_dscp/group10/tnp_trip*
mkdir -p /staging/groups/stat_dscp/group10/raw_csv

echo "Download 2018-2022"

#curl -L -o /staging/groups/stat_dscp/group10/raw_csv/2018.csv "https://pages.stat.wisc.edu/~krose/tnp_trips_2018_2022.csv"
curl -L -o /staging/groups/stat_dscp/group10/raw_csv/2018.csv "https://data.cityofchicago.org/api/views/m6dm-c72p/rows.csv?accessType=DOWNLOAD"

echo "Download 2023-2024"

#curl -L -o /staging/groups/stat_dscp/group10/raw_csv/2023.csv "https://pages.stat.wisc.edu/~krose/tnp_trips_2023_2024.csv"
curl -L -o /staging/groups/stat_dscp/group10/raw_csv/2023.csv "https://data.cityofchicago.org/api/views/n26f-ihde/rows.csv?accessType=DOWNLOAD"

echo "Download 2025"

#curl -L -o /staging/groups/stat_dscp/group10/raw_csv/2025.csv "https://pages.stat.wisc.edu/~krose/tnp_trips_2025.csv"
curl -L -o /staging/groups/stat_dscp/group10/raw_csv/2025.csv "https://data.cityofchicago.org/api/views/6dvr-xwnh/rows.csv?accessType=DOWNLOAD"


# Drop columns 6 (Percent Time Chicago), 7 (Percent Distance Chicago), and 17 (Shared Trip Match) due to 2018-2022 not having this data≈ß
echo "Dropping cols 6, 7, 17 from 2023 & 2025"

cut --complement -d',' -f6,7,17 /staging/groups/stat_dscp/group10/raw_csv/2023.csv > /staging/groups/stat_dscp/group10/raw_csv/tmp && mv /staging/groups/stat_dscp/group10/raw_csv/tmp /staging/groups/stat_dscp/group10/raw_csv/2023.csv
echo "Dropped Cols 2023"

cut --complement -d',' -f6,7,17 /staging/groups/stat_dscp/group10/raw_csv/2025.csv > /staging/groups/stat_dscp/group10/raw_csv/tmp && mv /staging/groups/stat_dscp/group10/raw_csv/tmp /staging/groups/stat_dscp/group10/raw_csv/2025.csv
echo "Dropped Cols 2025"

s1=$(stat -c%s /staging/groups/stat_dscp/group10/raw_csv/2018.csv)
s2=$(stat -c%s /staging/groups/stat_dscp/group10/raw_csv/2023.csv)
s3=$(stat -c%s /staging/groups/stat_dscp/group10/raw_csv/2025.csv)
sum=$((s1 + s2 + s3))

p1=$(( TOTAL_SPLITS * s1 / sum ))
p2=$(( TOTAL_SPLITS * s2 / sum ))
p3=$(( TOTAL_SPLITS - p1 - p2 ))

echo "Split proportions: 2018–22: $p1, 2023–24: $p2, 2025: $p3"

index=0

split_file() {
    f=$1
    num=$2

    echo "Split $f into $num parts"

    tail -n +2 "$f" | split -l $(( $(wc -l < "$f") / num + 1 )) - /staging/groups/stat_dscp/group10/tmp_

    for part in /staging/groups/stat_dscp/group10/tmp_*; do
       printf -v name "/staging/groups/stat_dscp/group10/tnp_trip_%02d.csv" "$index"
        mv "$part" "$name"
        index=$((index + 1))
    done

    rm -f "$f"
}

split_file /staging/groups/stat_dscp/group10/raw_csv/2018.csv $p1
split_file /staging/groups/stat_dscp/group10/raw_csv/2023.csv $p2
split_file /staging/groups/stat_dscp/group10/raw_csv/2025.csv $p3

rm -rf /staging/groups/stat_dscp/group10/raw_csv

echo "Create fileInputList"
ls -1 /staging/groups/stat_dscp/group10/tnp_trip_*.csv > fileInputList

echo "All files split into $TOTAL_SPLITS parts"
