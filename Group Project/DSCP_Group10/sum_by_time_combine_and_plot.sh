#!/bin/bash

output="sum_by_time_complete.csv"

# Concatenate all files, then group by time and sum counts
cat by_time/*_sum_by_time.csv | \
  sort | \
  awk -F',' '{
    gsub(/"/, "", $1);  # remove quotes from timestamp
    count[$1] += $2
  } END {
    for (time in count)
      printf "\"%s\",%d\n", time, count[time]
  }' | sort > "$output"

echo "Combined and grouped data written to $output"

echo "Now plot"
apptainer exec --bind "$PWD":"$PWD" \
  /staging/groups/stat_dscp/group10/python_numpy_pandas_sklearn_matplotlib.sif \
  python3 "$PWD/sum_by_time_plot.py"
