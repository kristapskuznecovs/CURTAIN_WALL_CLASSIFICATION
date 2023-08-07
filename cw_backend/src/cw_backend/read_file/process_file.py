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
    write_json.delete_files_in_folder(output_folder)

    start = time.time()

    files = sort_files.sort_files(filenames, current_dir)

    print('Files sorted in', time.time() - start)

    start = time.time()

    if len(files["unknown_files"]) > 0:
        print('Duplicate report files')
        for file in files["unknown_files"]:
            print(file)
        return False

    # Input
    opening_report = files["opening_file"]

    # profile_report = os.path.join(current_dir, 'Aile_Element_Classification', 'node_input', filename)
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
        # Get point cloud from Opening Report
        opening_data_tree = point_cloud.get_physical_opening_data_tree(opening_report)

    print('Generating openings, writing')
    print('Working...')

    # Call the function to delete the files

    write_json.delete_files_in_folder(json_folder)
    write_json.delete_files_in_folder(svg_folder)

    print('elements generated in ', time.time() - start)

    start = time.time()

    for element in elements:
        # try:
        for plane in element.element_planes:
            plane.generate_openings()

    for element in elements[:]:
        if not verification.left_or_right_side_as_single_profile(element):
            bad_elements.append(element)
            elements.remove(element)

    print('elements verified and openings generated in', time.time() - start)

    for element in elements:
        for plane in element.element_planes:
            if assign_opening_type:
                opening.find_opening_types_for_plane(plane, opening_data_tree)

        if draw_element:
            draw_svg.draw_element(element, svg_folder)
        if write_jsons:
            write_json.write_json(element, json_folder)

        # except:
        #     print('Problem', element.guid)
    if analyze_json:
        print('Analyzing JSONs')
        print('Working...')
        analyze_jsons.analyze_jsons(output_folder, json_folder)

        if settings["analyze_differences"]:
            analyze_element_difference.generate_report_of_similar_but_different_openings(json_folder,
                                                                                         output_folder,
                                                                                         difference_folder)

        # results[filename] = result  # Store the result using the filename as the key
        print('Finished')

    if len(bad_elements) > 0:
        print('\nBad Elements:')
        for element in bad_elements:
            print(element.guid)

    return True
