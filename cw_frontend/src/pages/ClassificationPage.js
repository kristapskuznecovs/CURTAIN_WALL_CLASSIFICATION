  import React, { useState } from 'react';
  import DropZone from '../components/DropZone';
  import ToastUpload from '../components/ToastUpload';
  import ButtonUpload from '../components/ButtonUpload';
  import './Text.css'

  const ClassificationPage = ({ showAlert }) => {
    const [uploadProgress, setUploadProgress] = useState(0);
    const [uploadedFileName, setUploadedFileName] = useState('');
    const [showToast, setShowToast] = useState(false);
    const [selectedFiles, setSelectedFiles] = useState([]);

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

    const handleFileRemove = (fileName) => {
      setSelectedFiles(prevSelectedFiles => prevSelectedFiles.filter(file => file.name !== fileName));
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
              selectedFiles={selectedFiles}
              setSelectedFiles={setSelectedFiles} // Pass the callback function to update selectedFiles
              setShowToast={setShowToast} // Pass setShowToast to the DropZone component
            />
          </div>
        </div>
        <div className=""> {/* Center the button */}
          <div className="col-md-12">
            <ButtonUpload
            fileName={uploadedFileName}
            handleFileUploadSuccess={handleFileUploadSuccess}
            selectedFiles={selectedFiles}
            />
          </div>
        </div>
        {showToast && ( // Render ToastUpload when showToast is true
          <ToastUpload
            show={showToast}
            handleClose={handleCloseToast}
            fileName={uploadedFileName}
            progress={uploadProgress}
            selectedFiles={selectedFiles} // Pass selectedFiles to ToastUpload
            handleFileRemove={handleFileRemove} // Pass the handleFileRemove function to the ToastUpload component
          />
        )}
      </div>
    );
    
  };

  export default ClassificationPage;