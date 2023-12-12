#!/bin/bash
# Checking Date format
if [ ! "$#" -eq 1 ]; then
  echo "Usage: This ETL only accepted ONE argument as date YYYY-DD-MM"
  exit 1
  fi
checking_date_format() {
  regex_pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
  if [[ ! $1 =~ $regex_pattern ]]; then
    echo "Usage: DATE argument in the wrong format, it must be YYYY-DD-MM"
    exit 1
  fi
}


# Condition Checking
function condition_checking {
  local format_user_app="user.application"
  local format_user_dev="user.device"
  local count_user_app_files=$(find . -maxdepth 1 -type f  -name "$format_user_app.${1}*.csv" | wc -l )
  local count_user_device_files=$(find .  -maxdepth 1 -type f  -name "$format_user_dev.${1}*.csv" | wc -l )
  if [ "$count_user_app_files" -ne 48 ]; then
    echo "user.application files not meet  threshold (must be 48)"
    echo "Current user_application files: ""$count_user_app_files"
    echo "The ETL process will be suspended"
    exit 1
    fi
  if [ "$count_user_device_files" -ne 48 ]; then
    echo "user.device files not meet threshold (must be 48)"
    echo "Current user_device files: ""$count_user_device_files"
    echo "The ETL process will be suspended"
    exit 1
    fi
    echo "Current user_application files: ""$count_user_app_files"
    echo "Current user_device files: ""$count_user_device_files"
}
condition_checking "$1"

echo "Processing: ..."
sort -u user.application."$1"*.csv | awk -F"," 'BEGIN {RS="\r\n"}  {OFS=", "} {count[$2]++} END { for (item in count) printf "%s%s%s\n", item, OFS, count[item] }' > application_unique_user_$1.csv
sort -u user.device."$1"*.csv | awk -F"," 'BEGIN {RS="\r\n"}  {OFS=", "} {count[$2]++} END { for (item in count) printf "%s%s%s\n", item, OFS, count[item] }' > device_unique_user_$1.csv






