import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
from flask import send_from_directory

import ReadCSV
import Write_Json
import DrawElement
import Opening
import PointCloud
import AnalyzeJsons

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')

"""
web - set to True for default use together with React
    - set to False to run in Python console for debug purposes
"""
web = True

accuracy = 1
profile_end_tolerance = 50
swap_bottom_profile = True

app = Flask(__name__)
CORS(app)  # Enable CORS support

results = {}  # Store the results

current_dir = os.getcwd()


@app.route('/')
def custom_index():
    return "Custom message goes here"


@app.route('/favicon.ico')
def ignore_favicon_request():
    return '', 204  # Return an empty response with a 204 status code (No Content)


@app.route('/getResults')
def get_results():
    return jsonify(results)


@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        # Access the uploaded file
        file = request.files['file']

        # Get the current directory path
        global current_dir

        # Construct the relative path to the 'node_input' directory
        node_input_dir = os.path.join(current_dir, 'node_input')

        # Create the 'node_input' directory if it doesn't exist
        if not os.path.exists(node_input_dir):
            os.makedirs(node_input_dir)

        # Save the file to the 'node_input' directory
        file.save(os.path.join(node_input_dir, file.filename))

        # Prepare the response message
        response = {
            'message': 'File uploaded and saved successfully',
            'filename': file.filename,
            'download_path': f'/api/download/{file.filename}'
        }

        # Trigger the processing logic
        try:
            result = process_files(file.filename)
            response['result'] = result
        except Exception as e:
            response['result'] = 'Processing error'
            logging.exception('Error during processing:')
            traceback.print_exc()

    except Exception as e:
        response = {
            'message': 'File upload failed',
            'error': str(e)
        }
        logging.exception('Error during file upload:')
        traceback.print_exc()

    # Return the response as JSON
    return jsonify(response)


def process_files(filename):
    global current_dir

    # Input
    opening_report = os.path.join(current_dir, 'node_input', 'GeelyOpeningData.csv')

    # profile_report = os.path.join(current_dir, 'Aile_Element_Classification', 'node_input', filename)
    profile_report = os.path.join(current_dir, 'node_input', filename)

    # Output
    json_folder = 'Results'
    output_folder = 'Output'
    write_jsons = True
    draw_element = False
    analyze_json = True
    assign_opening_type = True

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
    logging.debug(f'Result: {result}')
    return result


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    global current_dir
    output_folder = os.path.join(current_dir, 'Output')
    return send_from_directory(output_folder, 'output_grouping.csv')


@app.route('/api/download/filelist', methods=['GET'])
def get_file_names():
    output_folder = 'Output'
    filename_list = []
    for filename in os.listdir(output_folder):
        if os.path.isfile(os.path.join(output_folder, filename)):
            filename_list.append(filename)
    return filename_list


if __name__ == '__main__':
    if web:
        app.run()
    else:
        result = process_files("Geely_46.csv")
        print('Finished')
        # print(result)
