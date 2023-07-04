import os
import json
import csv
from itertools import zip_longest
import logging

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')


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


def get_opening_string(opening):
    result = ''
    if len(opening['CHILDREN']) == 0:
        try:
            result += ' TOP ' + opening['TOP']['PROFILE']
        except KeyError:
            pass

        try:
            result += ' BOTTOM ' + opening['BOTTOM']['PROFILE']
        except KeyError:
            pass

        try:
            result += ' LEFT ' + opening['LEFT']['PROFILE']
        except KeyError:
            pass

        try:
            result += ' RIGHT ' + opening['RIGHT']['PROFILE']
        except KeyError:
            pass

        result += '-' + str(opening["HEIGHT"])
        result += '-' + str(opening["WIDTH"])

        return ' OPENING: ' + result
    else:
        for child in opening['CHILDREN']:
            result += get_opening_string(child)
        return result


def get_opening_size_data(opening):
    result = ''
    if len(opening['CHILDREN']) == 0:
        height = opening["HEIGHT"]
        width = opening["WIDTH"]

        result += f'|{height} x {width}|'
        return result
    else:
        for child in opening['CHILDREN']:
            result += get_opening_size_data(child)
        return result


def get_opening_row_array(opening, result):
    if len(opening['CHILDREN']) == 0:
        try:
            top = opening['TOP']['GUID']
        except KeyError:
            top = 'None'

        try:
            bottom = opening['BOTTOM']['GUID']
        except KeyError:
            bottom = 'None'

        try:
            left = opening['LEFT']['GUID']
        except KeyError:
            left = 'None'

        try:
            right = opening['RIGHT']['GUID']
        except KeyError:
            right = 'None'

        try:
            type = opening['TYPE']
        except KeyError:
            type = 'None'
        try:
            location_dict = opening['LOCATION']
            origin = location_dict['ORIGIN']
            x_vector = location_dict['X_VECTOR']
            y_vector = location_dict['Y_VECTOR']
        except KeyError:

            logging.debug(f'No Location: {opening}')

            origin = None
            x_vector = None
            y_vector = None

        height = opening['HEIGHT']
        width = opening['WIDTH']

        row = [type, top, bottom, left, right, origin, x_vector, y_vector, height, width]

        result.append(row)
    else:
        for child in opening['CHILDREN']:
            get_opening_row_array(child, result)


def analyze_jsons(output_folder, json_folder):
    debug = False
    path = json_folder

    file_names = get_file_names(path)

    string_set = []
    opening_set = []
    string_id = {}
    string_guid_list = {}
    index = 1

    # Open the CSV file in write mode
    with open(output_folder + '\output_openings.csv', 'w', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['TYPE', 'TOP', 'BOTTOM', 'LEFT', 'RIGHT', 'ORIGIN', 'X_VECTOR', 'Y_VECTOR', 'HEIGHT', 'WIDTH'])

        for i in range(len(file_names)):

            file_name = file_names[i]

            if debug:
                print()
                print(file_name)

            file_path = os.path.join(path, file_name)

            if debug:
                print(file_path)

            with open(file_path) as f:
                data = json.load(f)
            guid = data['GUID']
            string = ''
            opening_data = ''
            for plane in data['PLANES']:
                opening = plane['OPENING']
                string += ' PLANE' + get_opening_string(opening)
                opening_data += get_opening_size_data(opening)
                row_array = []
                get_opening_row_array(opening, row_array)
                for row in row_array:
                    writer.writerow(row)

            # print(string)



            if string not in string_set:
                string_set.append(string)
                string_id[string] = index
                guid_list = []
                string_guid_list[index] = guid_list
                index += 1

            if opening_data not in opening_set:
                opening_set.append(opening_data)

            local_index = string_id[string]
            string_guid_list[local_index].append(guid)

    keys = string_guid_list.keys()


    group_dict = {}
    i = 1
    for key in keys:
        # print()
        guid_list = string_guid_list[key]
        group_dict[i] = guid_list
        i += 1
        length = len(guid_list)
        # print(f'{key},{length}')
        # for guid in guid_list:
        #     print(guid)

    # Open the CSV file in write mode
    with open(output_folder + '\output_grouping.csv', 'w', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file, delimiter=';')

        # Find the maximum length of the lists
        max_length = max(len(l) for l in string_guid_list.values())

        row = []
        for string in opening_set:
            string = string.replace('||', '|')
            row.append(string)
        writer.writerow(row)

        # Write the lists to separate columns in the CSV file
        for i in range(max_length):
            row = []
            for key in keys:
                guid_list = string_guid_list[key]
                if i < len(guid_list):
                    row.append(guid_list[i])
                else:
                    row.append('')

            writer.writerow(row)
    return group_dict
