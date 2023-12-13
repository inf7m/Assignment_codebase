import random
import csv

from datetime import datetime, timedelta

header = ["timestamp", "user UInt64", "app UInt64", "metric1 UInt64", "metric2 UInt64", "metric3 UInt64"]


# 6 fields

def create_timestamp_interval(date: str) -> list:
    interval = []
    date_formatted = datetime.strptime(date, "%Y-%m-%d")
    for i in range(48):
        interval_start = date_formatted + timedelta(minutes=i * 30)
        interval.append(interval_start)
    return interval


def generate_log_data(user_quantity: int, app_quantity: int) -> None:
    header = ["timestamp", "user", "app", "metric1", "metric2", "metric3"]
    data = []

    # Start/ End Date
    start_date_str = "2020-01-01"
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date_str = "2020-03-01"
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    current_date = start_date

    while current_date <= end_date:
        date_string = current_date.strftime("%Y-%m-%d")
        temporary_interval_timestamp = create_timestamp_interval(date_string)
        file_name = date_string + ".log.csv"
        file_path = "logs/"

        with open(file=file_path + file_name, mode='w', newline="") as logData:
            csv_writer = csv.writer(logData)
            csv_writer.writerow(header)

            for user_each in range(1, user_quantity + 1):  # Fixed the range
                for application in range(1, app_quantity + 1):
                    for interval_each in temporary_interval_timestamp:
                        data.append((interval_each, f"user{user_each}", f"app{application}",
                                 random.randint(1, 20000),
                                 random.randint(1, 12000),
                                 random.randint(1, 999)))

            csv_writer.writerows(data)

        # Move the reset of data list inside the loop to clear it for each date
        data = []
        current_date += timedelta(days=1)


generate_log_data(200, 2)
