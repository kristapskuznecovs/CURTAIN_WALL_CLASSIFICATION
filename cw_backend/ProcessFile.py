import os
import ReadCSV
import PointCloud
import Write_Json
import Opening
import DrawElement
import AnalyzeJsons

results = {}  # Store the results
current_dir = os.getcwd()

def process_files(filename):
    global current_dir

    # Input
    opening_report = os.path.join(current_dir, 'node_input', 'OpeningData.csv')

    # profile_report = os.path.join(current_dir, 'Aile_Element_Classification', 'node_input', filename)
    profile_report = os.path.join(current_dir, 'node_input', filename)

    # Output
    json_folder = 'Results'
    output_folder = 'Output'
    write_jsons = True
    draw_element = False
    analyze_json = True
    assign_opening_type = False

    # Group profiles by GUID's into distinct element objects
    elements = ReadCSV.read_csv(profile_report)

    if assign_opening_type:
        # Get point cloud from Opening Report
        point_cloud_array = PointCloud.get_point_cloud_array(opening_report)

    print('Generating openings, writing')
    print('Working...')

    # Call the function to delete the files
    Write_Json.delete_files_in_folder(json_folder)

    for element in elements:
        # try:
        for plane in element.element_planes:
            plane.generate_openings()
        for plane in element.element_planes:
            if assign_opening_type:
                Opening.assign_opening_type(plane.opening, plane.plane, point_cloud_array)
        if draw_element:
            DrawElement.draw_element(element)
        if write_jsons:
            Write_Json.write_json(element, json_folder)
        # except:
        #     print('Problem', element.guid)
    result = {"result": "This is an empty JSON"}
    if analyze_json:
        print('Analyzing JSONs')
        print('Working')
        result = AnalyzeJsons.analyze_jsons(output_folder, json_folder)
        results[filename] = result  # Store the result using the filename as the key
    return result
