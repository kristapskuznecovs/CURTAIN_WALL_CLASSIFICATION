import React from 'react';
import axios from 'axios';

const uploadFiles = async (formData, handleUploadProgress) => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // Set the content type explicitly
      },
      onUploadProgress: (progressEvent) => {
        const progress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
        handleUploadProgress(progress);
      },
    });
    console.log(response);
    // Handle the response or any additional logic
  } catch (error) {
    console.error('An error occurred during upload:', error);
    // Handle errors
  }
};

const ButtonUpload = ({ fileName }) => {
  const handleUpload = async () => {
    try {
      const formData = new FormData();
      formData.append('file', fileName); // Append the file to the FormData

      // Perform the upload action using the uploadFiles function
      await uploadFiles(formData, handleUploadProgress);
    } catch (error) {
      // Handle errors
      console.error('An error occurred during upload:', error);
    }
  };

  const handleUploadProgress = (progress) => {
    // Handle the progress update
    console.log('Upload progress:', progress);
  };

  return (
    <button
      type="button"
      className="btn button-sm btn-sm"
      onClick={handleUpload}
    >
      Take action
    </button>
  );
};

export default ButtonUpload;
