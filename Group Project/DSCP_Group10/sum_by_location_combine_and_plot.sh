#!/bin/bash

output_file="sum_by_location_complete.csv"

awk -F',' '
{
  # Key: year + coordinate
  key = $1 "," $2
  pickup[key] += $3
  dropoff[key] += $4
}
END {
  for (k in pickup) {
    printf "%s,%d,%d\n", k, pickup[k], dropoff[k]
  }
}
' by_location/*_sum_by_location.csv | sort -t',' -k1,1n -k3,3nr > "$output_file"

echo "Summed and combined data written to: $output_file"


apptainer exec --bind "$PWD":"$PWD" \
  /staging/groups/stat_dscp/group10/python_numpy_pandas_sklearn_matplotlib.sif \
  python3 "$PWD/sum_by_location_plot.py"
