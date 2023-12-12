#!/bin/bash
# Pre-check the argument number
if [ "$#" -ne 1 ]; then
 echo "Only ACCEPT ONE argument as parameter"
 exit 1
fi

function file_path_existed {
  local path_name=$1
  if [ ! -d "$path_name" ]; then
      echo "File Path Not existed!"
      exit 1
  fi
}
function checking_conditions {
    # Create the syslog location
    local path_name=$1
    local threshold_size_mb=1024
    for dir in "$path_name"/*/; do
      if (find . "$dir" -maxdepth 1 -type d  -name ".git" > /dev/null 2>&1) && [ "$(du -s -m $dir | awk '{print $1}')" -ge "$threshold_size_mb" ] ; then
        start_time=$(date +"%s")
        echo "$dir: $(du -s -m $dir | awk '{print $1/1024}') GB"
        end_time=$(date +"%s")
        duration_time=$(( (end_time - start_time) * 1000 ))"ms"
        echo $duration_time
          logger -t "ETL_exercise1" "Time needed for $dir: $duration_time"
        fi
      done
      }
file_path_existed $1
checking_conditions $1



