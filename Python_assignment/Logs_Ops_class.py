import csv
from datetime import datetime, timedelta
from pathlib import Path
import linecache
import os


def detecting_application_quantity(filename) -> int:
    number_of_lines = 1
    with open(filename, mode="r") as file:
        reader = csv.reader(file, delimiter=",")
        # Skip the header row
        header = next(reader)
        # Read the first data row
        first_data_row = next(reader)
        first_user_detect = first_data_row[1]
        for row in reader:
            current_user = row[1]
            if first_user_detect != current_user:
                break
            else:
                number_of_lines += 1
                continue
    return int(number_of_lines / 48)


def calculate_line_range_per_user(app_quantity) -> int:
    return app_quantity * 48


def aggregated_1day(file_path, line_start) -> list:
    application_quantity = detecting_application_quantity(filename=file_path)
    result = []
    total_sum3 = 0
    total_sum4 = 0
    total_sum5 = 0
    for line_number in range(line_start, line_start + (48 * application_quantity)):
        # Retrieve the specified line
        line = linecache.getline(file_path, line_number)
        # Use the csv module
        reader = csv.reader([line])
        row = next(reader)
        # Access the value then add it to the total sum
        column_value3 = float(row[3])
        column_value4 = float(row[4])
        column_value5 = float(row[5])

        total_sum3 += column_value3
        total_sum4 += column_value4
        total_sum5 += column_value5
    result.append(total_sum3)
    result.append(total_sum4)
    result.append(total_sum5)
    return result


def aggregated_1day_and_app(file_path, line_start) -> list:
    result = []
    total_sum3 = 0
    total_sum4 = 0
    total_sum5 = 0
    for line_number in range(line_start, line_start + 48):
        # Retrieve the specified line
        line = linecache.getline(file_path, line_number)
        # Use the csv module
        reader = csv.reader([line])
        row = next(reader)
        # Access the value then add it to the total sum
        column_value3 = float(row[3])
        column_value4 = float(row[4])
        column_value5 = float(row[5])

        total_sum3 += column_value3
        total_sum4 += column_value4
        total_sum5 += column_value5
    result.append(total_sum3)
    result.append(total_sum4)
    result.append(total_sum5)
    return result


def aggregated_30min_groupby(file_path, application_quantity, line_start) -> list:
    result_stack_metric1 = []
    result_stack_metric2 = []
    result_stack_metric3 = []
    result = []
    total_sum1 = 0
    total_sum2 = 0
    total_sum3 = 0
    for line_number in range(line_start, line_start + (48 * application_quantity)):
        # Retrieve the specified line from the CSV file
        line = linecache.getline(file_path, line_number)
        # Use the csv module to parse the line
        reader = csv.reader([line])
        row = next(reader)
        # Access the value in the specified column and add it to the total sum
        column_value1 = float(row[3])
        column_value2 = float(row[4])
        column_value3 = float(row[5])

        total_sum1 += column_value1
        total_sum2 += column_value2
        total_sum3 += column_value3

        result_stack_metric1.append(total_sum1)
        result_stack_metric2.append(total_sum2)
        result_stack_metric3.append(total_sum3)

    result.append(result_stack_metric1)
    result.append(result_stack_metric2)
    result.append(result_stack_metric3)
    return result


def offset_lines(app_name: str) -> int:
    format_app = app_name[3:]
    offset_by = 48 * (int(format_app) - 1)
    return offset_by


def define_user_start_line(file: str, user: str) -> int:
    application_quantity = detecting_application_quantity(filename=file)
    lines_from_each_user = (application_quantity * 48)
    user_number = int(user[4:]) - 1  # skip "app"
    return (user_number * lines_from_each_user) + 2  # for the header and from 0


def files_between_dates(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    file_list = os.listdir("logs")
    # Sort the list for files
    files_between = sorted(
        [
            os.path.join("logs", filename)
            for filename in file_list
            if os.path.isfile(os.path.join("logs", filename))
               and start_date <= datetime.strptime(filename.split('.')[0], "%Y-%m-%d") <= end_date
        ]
    )

    return files_between


class Logs_Ops_class:

    def __init__(self, log_directory):
        self.log_directory = Path(log_directory)
        self.log_data = self.load_logs()

    def load_logs(self):
        pass

    def query1(self, from_datetime: str, to_datetime: str, user, granularity: str):
        list_file = files_between_dates(start_date_str=from_datetime, end_date_str=to_datetime)
        if granularity == "30min":
            for file in list_file:
                start_line = define_user_start_line(file=file, user=user)
                line_per_user = calculate_line_range_per_user(
                    app_quantity=detecting_application_quantity(filename=file))
                end_line = start_line + line_per_user
                for line_number in range(start_line, end_line + 1):
                    line = linecache.getline(filename=file, lineno=line_number)  # using line-cache
                    print(line)
        elif granularity == "1day":
            for file in list_file:
                start_line = define_user_start_line(file=file, user=user)
                result = aggregated_1day(file_path=file, line_start=start_line)
                print(user + " " + file[5:15] + " 00:00:00," + str(result[0]) + "," + str(result[1]) + "," + str(
                    result[2]))  # reformat output
        else:
            print("""Only accept '30min' or '1hour' """)

    def query2(self, from_datetime: str, to_datetime: str, user: str, app: str, granularity: str):
        list_file = files_between_dates(start_date_str=from_datetime, end_date_str=to_datetime)
        if granularity == "30min":
            for file in list_file:
                start_line = define_user_start_line(file=file, user=user) + offset_lines(app_name=app)
                for line_number in range(start_line, start_line + 48):
                    line = linecache.getline(filename=file, lineno=line_number)  # using line-cache
                    print(line)
        elif granularity == "1day":
            for file in list_file:
                start_line = define_user_start_line(file=file, user=user)
                result = aggregated_1day_and_app(file_path=file, line_start=start_line)
                print(user + " " + file[5:15] + " 00:00:00," + str(result[0]) + "," + str(result[1]) + "," + str(
                    result[2]))  # reformat output
        else:
            print("""Only accept '30min' or '1hour' """)

    def query3(self, from_datetime: str, to_datetime: str, user: str, granularity: str, group_by: str):
        if group_by == "app":
            list_file = files_between_dates(start_date_str=from_datetime, end_date_str=to_datetime)
            if granularity == "30min":
                for file in list_file:
                    start_line = define_user_start_line(file=file, user=user)
                    application_quantity = detecting_application_quantity(filename=file)
                    user_start_line_start_from = define_user_start_line(file=file, user=user)
                    line_range = calculate_line_range_per_user(
                        app_quantity=application_quantity)
                    result = aggregated_30min_groupby(file_path=file, line_start=user_start_line_start_from,
                                                      application_quantity=application_quantity)
                    metric1 = result[0]
                    metric2 = result[1]
                    metric3 = result[2]
                    index = 0
                    for line_number in range(start_line, start_line + (line_range), 48):
                        line = linecache.getline(filename=file, lineno=line_number)  # using line-cache
                        print(line[0:30], metric1[index], metric2[index], metric3[index])
                        index += 1
            elif granularity == "1day":
                for file in list_file:
                    start_line = define_user_start_line(file=file, user=user)
                    application_quantity = detecting_application_quantity(filename=file)
                    user_start_line_start_from = define_user_start_line(file=file, user=user)
                    line_range = calculate_line_range_per_user(
                        app_quantity=application_quantity)
                    result = aggregated_30min_groupby(file_path=file, line_start=user_start_line_start_from,
                                                      application_quantity=application_quantity)
                    metric1 = result[0]
                    metric2 = result[1]
                    metric3 = result[2]
                    index = 0
                    for line_number in range(start_line, start_line + (line_range), 48):
                        line = linecache.getline(filename=file, lineno=line_number)  # using line-cache
                        print(line[0:30], metric1[index], metric2[index], metric3[index])
                        index += 48
            else:
                print("""Only accept '30min' or '1hour' """)
        else:
            print("Only support group by: app at this moment")


