import React, { useState } from 'react';
import axios from 'axios';

const UploadForm = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      await axios.post('/api/upload', formData);
      alert('File uploaded successfully!');
    } catch (error) {
      console.error(error);
      alert('An error occurred while uploading the file.');
    }
  };

  return (
    <div>
      <h2>Upload a CSV file</h2>
      <input type="file" onChange={handleFileChange} />
      <button className="btn btn-primary" onClick={handleUpload}>
        Upload
      </button>
    </div>
  );
};

export default UploadForm;
