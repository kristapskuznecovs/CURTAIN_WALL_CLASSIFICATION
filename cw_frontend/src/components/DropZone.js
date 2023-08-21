import React, { useCallback, useRef } from 'react';
import PropTypes from 'prop-types';
import { useDropzone } from 'react-dropzone'; 
import 'bootstrap/dist/css/bootstrap.min.css';
import './DropZone.css';
import './Buttons.css'

const DropZone = ({showAlert, selectedFiles, setSelectedFiles, setShowToast }) => {

  const handleFileSelection = useCallback((acceptedFiles) => {
    const newFiles = acceptedFiles.filter(file => {
      const fileExtension = file.name.split('.').pop().toLowerCase();
      return fileExtension === 'csv'; // Only allow CSV files
    });
  
    if (newFiles.length < acceptedFiles.length) {
      // Some files should be rejected because they are not CSV files
      const invalidFiles = acceptedFiles.filter(file => !newFiles.includes(file));
      showAlert('warning', `Tas nav CSV fails: ${invalidFiles.map(file => `"${file.name}"`).join(', ')}`);
    }
  
    const uniqueFiles = newFiles.filter(file => !selectedFiles.some(selectedFile => selectedFile.name === file.name));
    const duplicateFiles = newFiles.filter(file => selectedFiles.some(selectedFile => selectedFile.name === file.name));
  
    if (duplicateFiles.length > 0) {
      showAlert('warning', `Dublikātus nepieņemam: ${duplicateFiles.map(file => `"${file.name}"`).join(', ')}`);
    }
  
    if (uniqueFiles.length > 0) {
      setSelectedFiles(prevSelectedFiles => [...prevSelectedFiles, ...uniqueFiles]);
      setShowToast(true); // Show the toast when valid files are dropped
    }
  
  }, [selectedFiles, showAlert, setSelectedFiles, setShowToast]);
  
   const fileInputRef = useRef(null);

  const handleSelectButtonClick = () => {
    fileInputRef.current.click();
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: handleFileSelection,
    multiple: true,
  });

return (
    <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
      <input {...getInputProps({ accept: '.csv' })} />
      {isDragActive ? (
        <p className="">Pievienojiet failus šeit...</p>
      ) : (
        <div className="">
          <i className=""></i>
          <p className="">Nomet savu failu šeit</p>
          <button className="button" onClick={handleSelectButtonClick}>
            Izvēlies failu
          </button>
          {/* Hidden file input element */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => handleFileSelection(e.target.files)}
            style={{ display: 'none' }}
            accept=".csv"
            multiple
          />
        </div>
      )}
    </div>
  );
};

DropZone.propTypes = {
  showAlert: PropTypes.func.isRequired,
  setSelectedFiles: PropTypes.func.isRequired,
  setShowToast: PropTypes.func.isRequired,
};

export default DropZone;
