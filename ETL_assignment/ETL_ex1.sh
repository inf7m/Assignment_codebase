#!/bin/bash
# Pre-check the argument number
if [ "$#" -ne 1 ]; then
 echo "Only ACCEPT ONE argument as parameter"
 exit 1
fi

function file_path_existed {
  local path_name=$1
  if [ -d $path_name ]; then
    return 0 #TRUE
    else
      return 1 #FALSE
  fi
}
function checking_conditions {
    # Create the syslog location
    mkdir -p /var/log/ETL_mobileum_logs
    local LOG_pathname="/var/log/ETL_mobileum_logs/ETL_ex1.log"
    local path_name=$1
    local threshold_size_mb=1
    for dir in $path_name; do
      if find $dir -type d -maxdepth 1 -name ".git" && [ "$(du -s -m $dir | awk '{print $1}')" -ge "$threshold_size_mb" ] ; then
        start_time=$(date +"%Y-%m-%dT%H:%M:%S%z")
        echo "$dir: $(du -s -m $dir | awk '{print $1}')"
        duration_time=$start_time-$(date +"%Y-%m-%dT%H:%M:%S%z")
        logger -t "ETL_exercise1.log" "Time needed for $dir: $duration_time"
        fi
      done
      }
if file_path_existed $1; then
  checking_conditions $1
  else
    echo "File Path not Existed"
    exit 1
fi



