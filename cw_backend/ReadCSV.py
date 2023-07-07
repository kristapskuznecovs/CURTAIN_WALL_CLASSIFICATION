import csv
import Element
import Profile
import logging
import Verification

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

indexes = {"profile_index": 0,
           "length_index": 1,
           "start_x_index": 2,
           "start_y_index": 3,
           "start_z_index": 4,
           "end_x_index": 5,
           "end_y_index": 6,
           "end_z_index": 7,
           "part_guid_index": 8,
           "assembly_guid_index": 9,
           "delivery_number": 10
           }


def read_csv(file_path):
    # Method will go over each row of csv file.
    # First it looks at guid, if such element has already been created.
    # Second if, necessary it creates new element object and then adds profile to necessary element.
    previous_element_guid = set()
    elements = []

    with open(file_path, encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        # Skip first row (csv header)
        next(reader)

        for row in reader:

            assembly_guid = row[indexes["assembly_guid_index"]]

            # For AILE, "profiles" are beam elements AND cross-sections of those elements.
            profile = row[indexes["profile_index"]]

            length = float(row[indexes["length_index"]].replace(" ", ""))
            guid = row[indexes["part_guid_index"]]
            start_x = float(row[indexes["start_x_index"]].replace(" ", ""))
            start_y = float(row[indexes["start_y_index"]].replace(" ", ""))
            start_z = float(row[indexes["start_z_index"]].replace(" ", ""))
            end_x = float(row[indexes["end_x_index"]].replace(" ", ""))
            end_y = float(row[indexes["end_y_index"]].replace(" ", ""))
            end_z = float(row[indexes["end_z_index"]].replace(" ", ""))
            delivery_number = row[indexes["delivery_number"]]

            if assembly_guid not in previous_element_guid:
                previous_element_guid.add(assembly_guid)
                elements.append(Element.Element(assembly_guid))




            for element in elements:
                if element.guid == assembly_guid:
                    profile = Profile.Profile(profile, length, guid,
                                              start_x, start_y, start_z,
                                              end_x, end_y, end_z,
                                              delivery_number)
                    profile.start, profile.end = profile.end, profile.start
                    element.profiles.append(profile)

    elements, bad_elements = Verification.valid_or_invalid_elements(elements)

    if len(bad_elements) > 0:
        print('\nBad elements:')
        for element in bad_elements:
            print(element.guid)
        print()



    # After creation of element objects, profiles are split into element planes (necessary for corner elements)

    print(f'Read {len(elements)} elements from file')
    print('Working...')
    i = 0
    for element in elements:

        Element.assign_delivery_number(element)

        i += 1
        # print(i, element.guid)
        element.generate_planes()
        for plane in element.element_planes:
            plane.generate_size()
    print('Planes Generated')
    print('Working...')

    return elements
