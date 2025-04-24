#!/bin/bash

input_file="$1"

# Extract "96" from filename
suffix=$(basename "$input_file" | grep -o '[0-9]\+')

mkdir -p by_time
# Define output file
output_file="by_time/${suffix}_sum_by_time.csv"

# Extract column 2, count occurrences, keep full date-time, write to file
cut -d',' -f2 "$input_file" | \
  sort | \
  uniq -c | \
  sort -nr | \
  awk '{count=$1; $1=""; sub(/^ /, ""); print "\"" $0 "\"," count}' > "$output_file"

echo "Wrote counts to $output_file"
