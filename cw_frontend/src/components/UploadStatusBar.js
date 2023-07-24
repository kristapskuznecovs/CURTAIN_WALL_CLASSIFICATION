import React from 'react';

const UploadedFile = ({ fileName }) => {
  return (
    <div style={{ marginTop: '10px', fontSize: '16px' }}>
      <p>Uploaded File: {fileName}</p>
      {/* Additional rendering or functionality related to the uploaded file */}
    </div>
  );
};

export default UploadedFile;
