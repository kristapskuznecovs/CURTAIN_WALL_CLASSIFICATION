import os
import csv
from .. import settings


def sort_files(file_dict, directory):
    """
    Check file content, verify if all files correspond to necessary format
    :param file_dict: format {"files": []}
    :param directory: working directory folder (src/cw_backend)
    :return: dictionary of recognized files
    """

    input_folder = settings.settings["node_input"]

    file_names = file_dict["files"]
    file_paths = [os.path.join(directory, 'data', input_folder, file_name) for file_name in file_names]

    recognized_files = {"profile_file": None,
                        "opening_file": None,
                        "unknown_files": []}

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.reader(csv_file)
            first_line = next(csv_reader)

            # Hard coded checks regarding content of first line in reports

            if first_line == ['PROFILE;LENGTH / mm;START_X;START_Y;START_Z;END_X;END_Y;END_Z;'
                              'GUID;ASSEMBLY.GUID;DELIVERY_NUMBER']:
                if recognized_files["profile_file"] is None:
                    recognized_files["profile_file"] = file_path
                else:
                    recognized_files["unknown_files"].append(file_path)

            elif first_line == [
                    'NAME;ABREVIATION;CoG;ORIGIN;X;Y;Z;X_direction_size;Y_direction_size;GUID;ASSEMBLY_GUID']:
                if recognized_files["opening_file"] is None:
                    recognized_files["opening_file"] = file_path
                else:
                    recognized_files["unknown_files"].append(file_path)
            else:
                recognized_files["unknown_files"].append(file_path)

    settings.settings["assign_opening_type"] = recognized_files["opening_file"] is not None

    return recognized_files
