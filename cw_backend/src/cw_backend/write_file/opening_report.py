import os
import json
import csv


def get_file_names(directory_path):
    """
    USED!
    Gets all files in a directory
    :param directory_path:
    :return:
    """
    filename_list = []
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            filename_list.append(filename)
    return filename_list


def generate_opening_report(output_folder, json_folder):
    file_names = get_file_names(json_folder)

    output_openings_with_type_file_path = os.path.join(output_folder, "opening_report_type.csv")
    output_openings_without_type_file_path = os.path.join(output_folder, "opening_report_without_type.csv")

    print('Generating opening report')

    result_with_type = {}
    result_without_type = {}

    for i in range(len(file_names)):
        file_name = file_names[i]
        file_path = os.path.join(json_folder, file_name)

        with open(file_path) as f:
            data = json.load(f)

        for plane in data['PLANES']:
            opening = plane['OPENING']
            add_opening_to_result(opening, result_with_type, result_without_type)

    with open(output_openings_with_type_file_path, 'w', newline='') as file:
        keys = list(result_with_type.keys())
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Type', 'Size', 'Count'])
        for key in keys:
            count = result_with_type[key]
            info = key.split('|')
            size = info[0]
            type = info[1]
            row = [type, size, count]
            writer.writerow(row)

    with open(output_openings_without_type_file_path, 'w', newline='') as file:
        keys = list(result_without_type.keys())
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Size', 'Count'])
        for key in keys:
            count = result_without_type[key]
            row = [key, count]
            writer.writerow(row)


def add_opening_to_result(opening, result_with_type, result_without_type):
    height = round(opening["HEIGHT"], 1)
    width = round(opening["WIDTH"], 1)
    if "TYPE" in opening:
        type = opening["TYPE"]
    else:
        type = 'None'
    opening_result_with_type = f'{height} x {width} | {type}'
    opening_result_without_type = f'{height} x {width}'
    if opening_result_with_type not in result_with_type:
        result_with_type[opening_result_with_type] = 0
    result_with_type[opening_result_with_type] += 1

    if opening_result_without_type not in result_without_type:
        result_without_type[opening_result_without_type] = 0
    result_without_type[opening_result_without_type] += 1

    for child in opening["CHILDREN"]:
        add_opening_to_result(child, result_with_type, result_without_type)
