import React, { useState, useCallback } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import './Buttons.css';

const ButtonUpload = ({ selectedFiles }) => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = useCallback(async (formData) => {
    try {
      const response = await axios.post('http://192.168.20.195:5000/api/upload', formData, {
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
          setUploadProgress(progress);
        },
      });

      // Check the response status to determine if the upload was successful
      if (response.status === 200) {
        // Once the file is uploaded successfully, trigger the processing logic
        await triggerProcessing(response.data.filename);
      } else {
        // Handle the case when the response status is not 200
        console.error('File upload failed!');
      }
    } catch (error) {
      // Handle any errors that occurred during the API call
      console.error('An error occurred while uploading the file.', error);
    }
  }, []);

  const triggerProcessing = async (filename) => {
    try {
      // Call the API to trigger the file processing for the uploaded file
      const response = await axios.get(`http://192.168.20.195/api/process/${filename}`);
      // You can handle the response here if needed
      console.log('File processing response:', response.data);
    } catch (error) {
      // Handle any errors that occurred during the API call
      console.error('An error occurred while triggering file processing.', error);
    }
  };

  const handleButtonClick = async () => {
    try {
      // Upload all selected files
      for (const file of selectedFiles) {
        const formData = new FormData();
        formData.append('file', file);

        // Perform the upload action using the handleUpload function
        await handleUpload(formData);
      }
    } catch (error) {
      // Handle errors
      console.error('An error occurred during upload:', error);
    }
  };

  return (
    <button
      type="button"
      className={`button ${isUploading ? 'button-disabled' : ''}`} // Add the button-disabled class when isUploading is true
      onClick={handleButtonClick}
      disabled={isUploading} // Disable the button when isUploading is true
    >
      {isUploading ? 'Apstrādā...' : 'Augšupielādēt'}
    </button>
  );
};

ButtonUpload.propTypes = {
  selectedFiles: PropTypes.array.isRequired,
};

export default ButtonUpload;
