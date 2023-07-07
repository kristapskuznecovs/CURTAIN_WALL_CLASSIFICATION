import os
import json
import csv
from itertools import zip_longest
import logging

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')


def get_type_count(option1_list):
    """
    option1_list = list of {name, description}
    :param option1_list:
    :return: dictionary with description, it's key and quantity
    """
    unique_entries = set()


    i = 1
    objects = {}

    for entry in option1_list:

        description = entry["option1"]

        size = entry["option2"]

        if description not in unique_entries:
            unique_entries.add(description)

            objects[description] = {"count": 0, "key": i, "size_list": [], "size_count": {}}
            i += 1

        objects[description]["count"] += 1
        if size not in objects[description]["size_list"]:
            objects[description]["size_list"].append(size)
            objects[description]["size_count"][size] = 0
        objects[description]["size_count"][size] += 1


    descriptions = objects.keys()
    for description in descriptions:
        sizes = objects[description]["size_list"]
        i = 1
        size_dict = {}

        for size in sizes:
            size_dict[size] = i
            i+=1
        objects[description]["size_list"] = size_dict


    return objects


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


def get_opening_string_option1(opening):
    result = '['

    split_direction = opening["SPLIT DIRECTION"]

    if len(split_direction) > 0:
        result += str(len(opening["CHILDREN"]))

    result += split_direction

    if len(opening["SPLIT DIRECTION"]) > 0:
        result += ' '

    for children in opening["CHILDREN"]:
        result += get_opening_string_option1(children)

    if len(opening["CHILDREN"]) == 0:
        result += opening["TYPE"]
    result += '] '
    return result


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
    path = json_folder

    file_names = get_file_names(path)

    output_grouping_option1 = []

    # Open the CSV file in write mode
    with open(output_folder + '\output_openings.csv', 'w', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['TYPE', 'TOP', 'BOTTOM', 'LEFT', 'RIGHT', 'ORIGIN', 'X_VECTOR', 'Y_VECTOR', 'HEIGHT', 'WIDTH'])

        for i in range(len(file_names)):

            file_name = file_names[i]

            file_path = os.path.join(path, file_name)

            with open(file_path) as f:
                data = json.load(f)
            guid = data['GUID']

            delivery_number = data["DELIVERY_NUMBER"]

            string_option2 = f"{data['HEIGHT']} x {data['WIDTH']}"

            string = ''
            opening_data = ''
            string_option1 = ''
            i = 0
            for plane in data['PLANES']:
                i += 1
                string_option1 += f'P{i} '
                opening = plane['OPENING']
                string += ' PLANE' + get_opening_string(opening)
                opening_data += get_opening_size_data(opening)
                row_array = []
                get_opening_row_array(opening, row_array)
                for row in row_array:
                    writer.writerow(row)
                try:
                    string_option1 += get_opening_string_option1(opening)
                except:
                    print(f'There are problems with generating string option1 for {guid}')
            output_grouping_option1.append({"name": file_name, "option1": string_option1, "option2": string_option2, "delivery_number": delivery_number})

    types = get_type_count(output_grouping_option1)

    with open(output_folder + '\output_grouping.csv', 'w', newline='', encoding='UTF8') as file:

        writer = csv.writer(file, delimiter=';')

        writer.writerow(["NAME", "Option 1", "Option 1 description", "Option 2", "Option 2 Description"])
        for item in output_grouping_option1:
            name = item["delivery_number"]
            description = item["option1"]
            type = f'Group {types[description]["key"]}'

            size_description = item["option2"]
            size_type = types[description]["size_list"][size_description]

            size_group = f'Group {types[description]["key"]}-{size_type}'

            row = [name, type, description, size_group, size_description]
            writer.writerow(row)

    with open(output_folder + '\group_statistics.csv', 'w', newline='', encoding='UTF8') as file:
        writer = csv.writer(file, delimiter=';')

        writer.writerow(["TYPE", "TOTAL COUNT", "SPLIT INTO"])

        keys = types.keys()

        for key in keys:
            object = types[key]
            size_count = [key, object["count"]]

            sizes = object["size_count"].keys()

            for size in sizes:
                size_count.append(object["size_count"][size])




            writer.writerow(size_count)




    return types
