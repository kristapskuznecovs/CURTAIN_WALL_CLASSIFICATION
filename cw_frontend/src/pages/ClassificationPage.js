import React, { useState } from 'react';
import DropZone from '../components/DropZone';
import ToastUpload from '../components/ToastUpload';
import ButtonDownload from '../components/ButtonDownload';
import './Text.css'

const ClassificationPage = ({ showAlert }) => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedFileName, setUploadedFileName] = useState('');
  const [showToast, setShowToast] = useState(false);

  const handleUploadProgress = (progress) => {
    setUploadProgress(progress);
  };

  const handleFileUploadSuccess = (fileName) => {
    setUploadedFileName(fileName);
    setShowToast(true);
  };

  const handleShowToast = () => {
    setShowToast(true);
  };

  const handleCloseToast = () => {
    setShowToast(false);
  };

  return (
    <div className="full-screen-container">
      <div className="row">
        <div className="col-md-12">
          <h2 className="upload-heading">Pievieno fasādes failu</h2>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12">
          <DropZone             
            handleUploadProgress={handleUploadProgress}
            setUploadedFileName={setUploadedFileName}
            showAlert={showAlert}
            handleFileUploadSuccess={handleFileUploadSuccess}
          />
             <button className="button" onClick={() => setShowToast(true)}>Open Toast</button>
          <ToastUpload
            show={showToast}
            handleClose={handleCloseToast}
            fileName={uploadedFileName}
            progress={uploadProgress}
            />
        </div>
      </div>
    </div>
  );
};

export default ClassificationPage;