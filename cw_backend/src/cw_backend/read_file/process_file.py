import os
import time
from . import point_cloud, read_profile_csv
from ..write_file import draw_svg, analyze_element_difference, analyze_jsons
from ..write_file import write_json
from ..classes.element_representation import opening
from .. import settings
from ..errors import error_handling
from ..errors import verification
from ..read_file import sort_files
from tqdm import tqdm
from ..write_file import error_log
from ..classes.other import geometry

results = {"Errors": error_handling.errors}  # Store the results

settings = settings.settings

current_dir = ''


def set_current_directory(current_directory):
    global current_dir
    current_dir = current_directory


def process_files(filenames):
    global current_dir

    output_folder = os.path.join(current_dir, 'data', settings["output_folder"])

    print('Deleting output files')
    write_json.delete_files_in_folder(output_folder)

    files = sort_files.sort_files(filenames, current_dir)

    if len(files["unknown_files"]) > 0:
        print('Bad report files')
        for file in files["unknown_files"]:
            print(file)
        return False

    # Input
    opening_report = files["opening_file"]
    profile_report = files["profile_file"]

    # Output
    json_folder = os.path.join(current_dir, 'data', settings["json_folder"])
    svg_folder = os.path.join(current_dir, 'data', settings["svg_folder"])
    write_jsons = settings["write_jsons"]
    draw_element = settings["draw_element"]
    analyze_json = settings["analyze_json"]
    difference_folder = os.path.join(current_dir, 'data', settings["difference_results"])

    assign_opening_type = settings["assign_opening_type"]

    # Group profiles by GUID's into distinct element objects
    elements, bad_elements = read_profile_csv.read_csv(profile_report)

    if not elements:
        return False

    if assign_opening_type:
        # Get physical opening list
        opening_data_tree = point_cloud.get_physical_opening_data_tree(opening_report, elements, bad_elements)





    # Call the function to delete the files

    print('Deleting json files')
    write_json.delete_files_in_folder(json_folder)
    print('Deleting svg files')
    write_json.delete_files_in_folder(svg_folder)

    start = time.time()



    for element in elements:
        # try:
        for plane in element.element_planes:
            plane.generate_openings()

    for element in elements[:]:
        if not verification.left_or_right_side_as_single_profile(element):
            bad_elements.append(element)
            elements.remove(element)

    print('Assigning opening type, creating svg, json')
    for element in tqdm(elements):
        for plane in element.element_planes:
            if assign_opening_type:
                opening.find_opening_types_for_plane(plane, opening_data_tree, element.physical_openings)

        if draw_element:
            draw_svg.draw_element(element, svg_folder)
        if write_jsons:
            write_json.write_json(element, json_folder)

        # except:
        #     print('Problem', element.guid)
    if analyze_json:

        analyze_jsons.analyze_jsons(output_folder, json_folder)

        if settings["analyze_differences"]:
            analyze_element_difference.generate_report_of_similar_but_different_openings(json_folder,
                                                                                         output_folder,
                                                                                         difference_folder)

    if len(bad_elements) > 0:
        print(f'\n{len(bad_elements)} Bad Elements')
        error_log.write_error_log(bad_elements, output_folder)

    print('Finished')

    return True
