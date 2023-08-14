import csv
from ..classes.other import geometry
from ..classes.element_representation import opening as opening_module


def transform_raw_to_point(data):
    data = data.replace('{', '')
    data = data.replace('}', '')
    data = [round(float(x.rstrip()), 1) for x in data.split(',')]
    point = geometry.Point(data[0], data[1], data[2])
    return point


def transform_raw_to_vector(data):
    data = data.replace('{', '')
    data = data.replace('}', '')
    data = [round(float(x.rstrip()), 1) for x in data.split(',')]
    vector = geometry.Vector(data[0], data[1], data[2])
    return vector


def read_opening_csv(file_path):
    # Method will go over each row of csv file.
    # First it looks at guid, if such element has already been created.
    # Second if, necessary it creates new element object and then adds profile to necessary element.

    indexes = {"name": 0,
               "opening_type": 1,
               "cog": 2,
               "origin": 3,
               "x_vector": 4,
               "y_vector": 5,
               "z_vector": 6,
               "height": 7,
               "width": 8,
               "guid": 9,
               "assembly_guid": 10}

    name_index = indexes["name"]
    opening_type_index = indexes["opening_type"]
    cog_index = indexes["cog"]
    origin_index = indexes["origin"]
    x_index = indexes["x_vector"]
    y_index = indexes["y_vector"]
    z_index = indexes["z_vector"]
    height_index = indexes["height"]
    width_index = indexes["width"]
    guid_index = indexes["guid"]
    assembly_guid_index = indexes["assembly_guid"]

    openings = []

    with open(file_path, encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        # Skip first row (csv header)
        next(reader)

        for row in reader:

            name = row[name_index]
            opening_type = row[opening_type_index]
            cog = transform_raw_to_point(row[cog_index])
            origin = transform_raw_to_point(row[origin_index])
            x_vector = transform_raw_to_vector(row[x_index])
            y_vector = transform_raw_to_vector(row[y_index])
            z_vector = transform_raw_to_vector(row[z_index])
            height = float(row[height_index])
            width = float(row[width_index])
            guid = row[guid_index]
            assembly_guid = row[assembly_guid_index]

            new_plane = geometry.Plane(origin, x_vector, y_vector)

            new_opening = opening_module.Opening(height, width, origin, [], new_plane, 0)

            new_opening.guid = guid
            new_opening.type = opening_type
            new_opening.name = name
            new_opening.center = cog
            new_opening.assembly_guid = assembly_guid

            openings.append(new_opening)

    return openings
