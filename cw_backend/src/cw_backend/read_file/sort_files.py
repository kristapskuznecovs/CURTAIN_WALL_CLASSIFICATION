import os
import csv
from .. import settings


def sort_files(file_dict, directory):
    input_folder = settings.settings["node_input"]

    file_names = file_dict["files"]
    file_paths = []
    for file_name in file_names:
        file_paths.append(os.path.join(directory, 'data', input_folder, file_name))

    file_name_dict = {"profile_file": None,
                      "opening_file": None,
                      "unknown_files": []}

    for file in file_paths:
        with open(file, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            first_line = next(csv_reader)
            if first_line == ['PROFILE;LENGTH / mm;START_X;START_Y;START_Z;END_X;END_Y;END_Z;'
                              'GUID;ASSEMBLY.GUID;DELIVERY_NUMBER']:
                if file_name_dict["profile_file"] is None:
                    file_name_dict["profile_file"] = file
                else:
                    file_name_dict["unknown_files"].append(file)
            elif first_line == ['NAME;ABREVIATION;CoG;ORIGIN;X;Y;Z;X_direction_size;Y_direction_size;GUID;ASSEMBLY_GUID']:
                if file_name_dict["opening_file"] is None:
                    file_name_dict["opening_file"] = file
                else:
                    file_name_dict["unknown_files"].append(file)
            else:
                file_name_dict["unknown_files"].append(file)
    return file_name_dict
