import json
import os


def write_error_log(bad_elements, output_folder):
    result = {}

    for element in bad_elements:
        error = element.error
        delivery_number = element.delivery_number
        guid = element.guid
        if element.error not in result:
            result[error] = {"GUID": [], "DELIVERY_NUMBER": []}
        result[error]["GUID"].append(guid)
        result[error]["DELIVERY_NUMBER"].append(delivery_number)

    json_data = json.dumps(result, indent=4)

    error_log_file = os.path.join(output_folder, 'error_log.json')

    with open(error_log_file, "w") as file:
        file.write(json_data)
