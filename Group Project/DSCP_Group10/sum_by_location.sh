#!/bin/bash

input_file="$1"

# Extract numeric suffix (e.g., "96" from "tnp_trip_96.csv")
suffix=$(basename "$input_file" | grep -o '[0-9]\+')

mkdir -p by_location
# Output file
output_file="by_location/${suffix}_sum_by_location.csv"

awk -F',' '
BEGIN { OFS="," }
{
  # Extract year from timestamp (col 2), expected format "MM/DD/YYYY HH:MM:SS AM/PM"
  split($2, datetime, " ")
  split(datetime[1], date_parts, "/")
  year = date_parts[3]

  # Count pickup and dropoff by (year, coordinate)
  pickup_key = year "|" $18
  dropoff_key = year "|" $21

  pickup[pickup_key]++
  dropoff[dropoff_key]++
}
END {
  for (key in pickup) {
    split(key, parts, "|")
    year = parts[1]
    coord = parts[2]
    all_keys[year "|" coord] = 1
  }
  for (key in dropoff) {
    all_keys[key] = 1
  }

  for (key in all_keys) {
    split(key, parts, "|")
    year = parts[1]
    coord = parts[2]
    printf "\"%s\",\"%s\",%d,%d\n", year, coord, pickup[key]+0, dropoff[key]+0
  }
}
' "$input_file" | sort -t',' -k1,1n -k3,3nr > "$output_file"

echo "Wrote output to $output_file"
