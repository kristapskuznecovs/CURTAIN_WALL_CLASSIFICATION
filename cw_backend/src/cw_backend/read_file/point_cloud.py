from . import read_openings_csv
from ..classes.other import geometry


def get_physical_opening_data_tree(opening_report, good_elements, bad_elements):
    # Get point cloud from Opening Report
    openings = read_openings_csv.read_opening_csv(opening_report)
    print(f'From report read {len(openings)} items')

    elements = good_elements + bad_elements
    elements_by_guid = {}

    for element in elements:
        elements_by_guid[element.guid] = element

    openings_not_assigned_to_element = []
    for opening in openings:
        if opening.assembly_guid in elements_by_guid:
            elements_by_guid[opening.assembly_guid].physical_openings.append(opening)
        else:
            openings_not_assigned_to_element.append(opening)

    sorted_not_assigned_openings = sorted(openings_not_assigned_to_element, key=lambda opening: geometry.distance_to_zero(opening.center))

    opening_data_tree = {0: []}

    i = 0

    while len(sorted_not_assigned_openings) > 1:
        i += 1000
        current_list = []
        opening_data_tree[i] = current_list
        while True:
            if len(sorted_not_assigned_openings) == 0:
                break
            if geometry.distance_to_zero(sorted_not_assigned_openings[0].center) < i:
                current_list.append(sorted_not_assigned_openings.pop(0))
            else:
                break

    opening_data_tree[i + 1000] = []

    opening_data_tree["max"] = i + 1000

    print('Working...')

    return opening_data_tree
