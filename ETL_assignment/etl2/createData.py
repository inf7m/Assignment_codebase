import random
import csv


def generate_random_data_user_app(num_entries):
    data = []
    for _ in range(num_entries):
        data.append([
            "user" + str(random.randint(1, 120000)),
            " application" + str(random.randint(1, 120))
        ])
    return data


def generate_random_data_user_device(num_entries):
    data = []
    for _ in range(num_entries):
        data.append([
            "user" + str(random.randint(1, 120000)),
            "device" + str(random.randint(1, 120))
        ])
    return data


def write_to_csv(data, filename):
    with open(filename, mode='w', newline="") as csvData:
        csv_writer = csv.writer(csvData)
        for i in range(1, 15):
            csv_writer.writerows(data)


if __name__ == "__main__":
    num_entries = 100000
    user_application_prefix = "user.application.2023-01-01-"
    user_device_prefix = "user.device.2023-01-01-"
    hours_list = list(range(24))
    formatted_hours_list = [f"{hour:02}" for hour in hours_list]
    mins_interval_list = ["00", "30"]
    for i in range(len(formatted_hours_list)):
        write_to_csv(generate_random_data_user_app(num_entries),
                     user_application_prefix
                     + str(formatted_hours_list[i])
                     + "-"
                     + str(mins_interval_list[0])
                     + ".csv")
        write_to_csv(generate_random_data_user_device(num_entries),
                     user_device_prefix
                     + str(formatted_hours_list[i])
                     + "-"
                     + str(mins_interval_list[0])
                     + ".csv")
        write_to_csv(generate_random_data_user_app(num_entries),
                     user_application_prefix
                     + str(formatted_hours_list[i])
                     + "-"
                     + str(mins_interval_list[1])
                     + ".csv")
        write_to_csv(generate_random_data_user_device(num_entries),
                     user_device_prefix
                     + str(formatted_hours_list[i])
                     + "-"
                     + str(mins_interval_list[1])
                     + ".csv")
