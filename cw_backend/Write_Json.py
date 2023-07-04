import json
import logging

import main

accuracy = main.accuracy

# Set up logging configuration
logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')


def write_json(element, json_folder):
    # create a Python dictionary with some data

    guid = element.guid
    height = round(element.element_planes[0].height, accuracy)
    width = 0
    for plane in element.element_planes:
        width += plane.width
    width = round(width, accuracy)
    plane_count = element.plane_count

    planes = []

    def get_children_data(opening):
        opening_dict = {}
        opening_dict["HEIGHT"] = round(opening.height, accuracy)
        opening_dict["WIDTH"] = round(opening.width, accuracy)
        opening_plane = opening.local_opening_plane
        opening_dict["LOCATION"] = {"ORIGIN": opening_plane.get_origin_str(),
                                    "X_VECTOR": opening_plane.get_x_vec_str(),
                                    "Y_VECTOR": opening_plane.get_y_vec_str()}

        opening_dict["LEVEL"] = opening.level

        if opening.top is not None:
            opening_dict["TOP"] = {"PROFILE": opening.top.profile, "GUID": opening.top.guid}
        if opening.bottom is not None:
            opening_dict["BOTTOM"] = {"PROFILE": opening.bottom.profile, "GUID": opening.bottom.guid}
        if opening.left is not None:
            opening_dict["LEFT"] = {"PROFILE": opening.left.profile, "GUID": opening.left.guid}
        if opening.right is not None:
            opening_dict["RIGHT"] = {"PROFILE": opening.right.profile, "GUID": opening.right.guid}

        opening_dict["CHILDREN"] = []

        if len(opening.children) == 0:
            opening_dict["TYPE"] = opening.type

        for child_opening in opening.children:
            opening_dict["CHILDREN"].append(get_children_data(child_opening))

        return opening_dict

    for plane in element.element_planes:
        plane_dict = {}
        plane_dict["HEIGHT"] = round(plane.height, accuracy)
        plane_dict["WIDTH"] = round(plane.width, accuracy)

        opening = plane.opening

        opening_dict = {}

        opening_dict["HEIGHT"] = round(opening.height, accuracy)
        opening_dict["WIDTH"] = round(opening.width, accuracy)

        opening_plane = opening.plane
        opening_dict["LOCATION"] = {"ORIGIN": opening_plane.get_origin_str(),
                                    "X_VECTOR": opening_plane.get_x_vec_str(),
                                    "Y_VECTOR": opening_plane.get_y_vec_str()}

        opening_dict["LEVEL"] = opening.level

        if opening.top is not None:
            opening_dict["TOP"] = {"PROFILE": opening.top.profile, "GUID": opening.top.guid}
        if opening.bottom is not None:
            opening_dict["BOTTOM"] = {"PROFILE": opening.bottom.profile, "GUID": opening.bottom.guid}
        if opening.left is not None:
            opening_dict["LEFT"] = {"PROFILE": opening.left.profile, "GUID": opening.left.guid}
        if opening.right is not None:
            opening_dict["RIGHT"] = {"PROFILE": opening.right.profile, "GUID": opening.right.guid}

        opening_dict["CHILDREN"] = []

        for child_opening in opening.children:
            opening_dict["CHILDREN"].append(get_children_data(child_opening))

        plane_dict["OPENING"] = opening_dict

        planes.append(plane_dict)

    data = {
        "GUID": guid,
        "HEIGHT": height,
        "WIDTH": width,
        "PLANE COUNT": plane_count,
        "PLANES": planes
    }

    # serialize the data to JSON format

    json_data = json.dumps(data, indent=4)

    # create a new file and write the JSON data to it
    file_path = json_folder + '/' + guid + '.json'

    with open(file_path, "w") as file:
        file.write(json_data)
