#!/bin/bash
if [ ! "$#" -eq 2 ]; then
  echo "Usage: This ETL only accepted ONE argument as date YYYY-DD-MM"
  exit 1
  fi
# Prevent condition the program hanging if not found
if [ ! -f "user.application.$1.csv" ]; then
      echo "File Path Not existed!"
      exit 1
fi

checking_date_format() {
  regex_pattern="^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
  if [[ ! $1 =~ $regex_pattern ]]; then
    echo "Usage: DATE argument in the wrong format, it must be YYYY-DD-MM"
    exit 1
  fi
}
checking_date_format "$1"
# Identify oldest date user_application file
oldest_file=$(ls -lt --time=creation | grep "user.application" | awk 'NR==1 {print $NF}')
# Identify current date user_application file and prevent the program hanging if not found
provided_date_file="user.application.$1.csv"
if [ -f "$current_date_provided_file" ]; then
  echo "Dont have any files with the provided date "
  exit 1
  fi
# Identify latest user_application file
latest_date_provided_file=$(ls -lt --time=creation | grep "user.application" | awk 'END {print $NF}')
# Extract to get date only - using for UNIX Timestamp Convention
extract_date_oldest_date="${oldest_file:17:10}"
extract_date_provided_date="${provided_date_file:17:10}"
extract_date_latest_date="${latest_date_provided_file:17:10}"
function calculation_days_between {
  # Convert dates to Unix timestamps
  timestamp1=$(date -d "$extract_date_oldest_date" +%s)
  timestamp2=$(date -d "$extract_date_provided_date" +%s)
  # Calculate the difference in seconds
  difference=$((timestamp2 - timestamp1))
  # Convert the difference to days
  days=$((difference / 86400))  # 86400 seconds in a day
  echo "$days"
}
occurrences=$(($(calculation_days_between) + 1 ))
# Find files between the start and end dates
readarray -t file_paths < <(find . -type f -name "user.application.*.csv" -printf "%P\n")

function get_files_between_oldest_and_provided {
  local files_in_date_range=()
  local timestamp_oldest_file=$(date -d "$extract_date_oldest_date" +%s)
  local convert_int_time_oldest=$((timestamp_oldest_file + 0))
  local timestamp_provided_file=$(date -d "$extract_date_provided_date" +%s)
  local convert_int_time_provided=$((timestamp_provided_file + 0))
  # Process the identified files
  for file in "${file_paths[@]}"; do
    local extract_date=$(echo "$file" | awk -F'.' '{print $3}')
    local timestamp_each=$(date -d "$extract_date" +%s)
    local convert_int_time_each=$((timestamp_each + 0))
    if [ "$convert_int_time_each" -ge "$convert_int_time_oldest" ] && [ "$convert_int_time_each" -le "$convert_int_time_provided" ]; then
        files_in_date_range+=("$file")
  fi
    done
  echo "${files_in_date_range[@]}"
}
function get_files_between_provided_and_latest {
  local files_in_date_range=()
  local timestamp_latest_file=$(date -d "$extract_date_latest_date" +%s)
  local convert_int_time_latest=$((timestamp_latest_file + 0))
  local timestamp_provided_file=$(date -d "$extract_date_provided_date" +%s)
  local convert_int_time_provided=$((timestamp_provided_file + 0))
  # Process the identified files
  for file in "${file_paths[@]}"; do
    local extract_date=$(echo "$file" | awk -F'.' '{print $3}')
    local timestamp_each=$(date -d "$extract_date" +%s)
    local convert_int_time_each=$((timestamp_each + 0))
    if [ "$convert_int_time_each" -gt "$convert_int_time_provided" ] && [ "$convert_int_time_each" -le "$convert_int_time_latest" ]; then
        files_in_date_range+=("$file")
  fi
    done
  echo "${files_in_date_range[@]}"
}

# Get the list of files for conditions
file_in_date_range_oldest_provided=$(get_files_between_oldest_and_provided)
file_in_date_range_provided_latest=$(get_files_between_provided_and_latest)

awk -F"," -v threshold_occurrences="$occurrences" -v target_value="$2" '{OFS=","} $2 == target_value { users[$1]++ } END { for (item in users) { if (users[item] == threshold_occurrences) printf "%s\n", item } }' ${file_in_date_range_oldest_provided[@]} > condition1.temp
awk -F"," -v threshold_occurrences="1" -v target_value="$2" '{OFS=","} $2 == target_value { users[$1]++ } END { for (item in users) { if (users[item] >= threshold_occurrences) printf "%s\n", item } }' ${file_in_date_range_provided_latest[@]} > condition2.temp
echo "The list of users using [ $2 ] every day up to the $1 and never used it from $1 are:"

# Combination from both .temp files (first and second) finalize step
comm -23 <(sort condition1.temp) <(sort condition2.temp)
# Remove the .temp files
rm condition1.temp condition2.temp