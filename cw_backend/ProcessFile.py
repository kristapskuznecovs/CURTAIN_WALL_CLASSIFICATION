import os
import ReadCSV
import PointCloud
import Write_Json
import Opening
import DrawElement
import AnalyzeJsons
import Settings
import AnalyzeElementDifferences

results = {}  # Store the results


settings = Settings.settings

current_dir = ''


def set_current_directory(current_directory):
    global current_dir
    current_dir = current_directory


def process_files(filename):
    global current_dir

    # Input
    opening_report = os.path.join(current_dir, 'node_input', 'OpeningData.csv')

    # profile_report = os.path.join(current_dir, 'Aile_Element_Classification', 'node_input', filename)
    profile_report = os.path.join(current_dir, 'node_input', filename)

    # Output
    json_folder = os.path.join(current_dir, settings["json_folder"])


    output_folder = os.path.join(current_dir, settings["output_folder"])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    svg_folder = os.path.join(current_dir, settings["svg_folder"])
    write_jsons = settings["write_jsons"]
    draw_element = settings["draw_element"]
    analyze_json = settings["analyze_json"]

    difference_folder = os.path.join(current_dir, settings["difference_results"])
    if not os.path.exists(difference_folder):
        os.makedirs(difference_folder)

    assign_opening_type = settings["assign_opening_type"]

    # Group profiles by GUID's into distinct element objects
    elements = ReadCSV.read_csv(profile_report)

    if assign_opening_type:
        # Get point cloud from Opening Report
        point_cloud_array = PointCloud.get_point_cloud_array(opening_report)

    print('Generating openings, writing')
    print('Working...')

    # Call the function to delete the files
    if not os.path.exists(json_folder):
        os.makedirs(json_folder)

    Write_Json.delete_files_in_folder(json_folder)

    if not os.path.exists(svg_folder):
        os.makedirs(svg_folder)

    Write_Json.delete_files_in_folder(svg_folder)

    for element in elements:
        # try:
        for plane in element.element_planes:
            plane.generate_openings()
        for plane in element.element_planes:
            if assign_opening_type:
                Opening.assign_opening_type(plane.opening, plane.plane, point_cloud_array)
        if draw_element:
            DrawElement.draw_element(element, svg_folder)
        if write_jsons:
            Write_Json.write_json(element, json_folder)
        # except:
        #     print('Problem', element.guid)
    result = {"result": "This is an empty JSON"}
    if analyze_json:
        print('Analyzing JSONs')
        print('Working')
        result = AnalyzeJsons.analyze_jsons(output_folder, json_folder)

        if settings["analyze_differences"]:
            AnalyzeElementDifferences.generate_report_of_similar_but_different_openings(json_folder,
                                                                                        output_folder,
                                                                                        difference_folder)

        results[filename] = result  # Store the result using the filename as the key
    return result
