#!/bin/bash

# Specify the target directory
target_directory="/Users/sebastian/PycharmProjects/Mobileum"

# Initialize counter variable
subdirectory_count=0

# Loop through subdirectories using find
for subdirectory in "$target_directory"/*/; do
    if [ -d "$subdirectory" ]; then
        # Increment the counter for each subdirectory
        echo $subdirectory
        ((subdirectory_count++))
    fi
done

# Print the final count
echo "Number of subdirectories in $target_directory: $subdirectory_count"
