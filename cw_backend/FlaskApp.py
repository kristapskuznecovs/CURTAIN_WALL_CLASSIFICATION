from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
from flask import send_from_directory
import os
import logging

import ProcessFile
import Settings

app = Flask(__name__)
CORS(app)  # Enable CORS support

results = ProcessFile.results  # Store the results


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

        # Construct the relative path to the 'node_input' directory
        node_input_dir = os.path.join('node_input')

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

    except Exception as e:
        response = {
            'message': 'File upload failed',
            'error': str(e)
        }
        logging.exception('Error during file upload:')
        traceback.print_exc()

    # Return the response as JSON
    return jsonify(response)


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    output_folder = os.path.join('Output')
    return send_from_directory(output_folder, 'output_grouping.csv')


@app.route('/api/download/filelist', methods=['GET'])
def get_file_names():
    output_folder = 'Output'
    filename_list = []
    for filename in os.listdir(output_folder):
        if os.path.isfile(os.path.join(output_folder, filename)):
            filename_list.append(filename)
    return filename_list


@app.route('/api/delete/<folder>/<filename>', methods=['DELETE'])
def delete_file(folder, filename):
    path = os.path.join(folder, filename)
    if os.path.isfile(path):
        try:
            os.remove(path)
            return "File deleted"
        except Exception as e:
            return "Error: File not deleted"
    else:
        return 'File not found'


@app.route('/api/process/<filename>', methods=['GET'])
def run_process_file(filename):
    response = {
        'message': 'File processed successfully',
        'filename': filename,
    }
    # Trigger the processing logic
    try:
        result = ProcessFile.process_files(filename)
        response['result'] = result

    except Exception as e:
        response['result'] = 'Processing error'
        logging.exception('Error during processing:')
        traceback.print_exc()

    return response


@app.route('/api/settings/<settings>', methods=['POST'])
def set_settings(settings):
    try:
        Settings.settings = settings
        return True
    except Exception as e:
        traceback.print_exc()
        return False
