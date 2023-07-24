import React from 'react';
import axios from 'axios';

const ButtonUpload = ({ fileName }) => {
  const handleUpload = async () => {
    try {
      // Perform the upload action using axios or any other HTTP library
      const response = await axios.post('http://127.0.0.1:5000/api/upload', { fileName });
      // Handle the response or any additional logic
      console.log(response);
    } catch (error) {
      // Handle errors
      console.error('An error occurred during upload:', error);
    }
  };

  return (
    <button type="button" className="btn button-sm btn-sm" onClick={handleUpload}>
      Take action
    </button>
  );
};

export default ButtonUpload;
