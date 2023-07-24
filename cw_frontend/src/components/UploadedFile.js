import React from 'react';

const UploadedFile = ({ fileName }) => {
  console.log("fileName:", fileName); // Add console log here
  
  return (
    <div style={{ marginTop: '', fontSize: '' }}>
      <p>Uploaded File: {fileName}</p>
      {/* Additional rendering or functionality related to the uploaded file */}
    </div>
  );
};

export default UploadedFile;
