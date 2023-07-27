import React, { useCallback, useState, useRef } from 'react';
import PropTypes from 'prop-types';
import { useDropzone } from 'react-dropzone';
import 'bootstrap/dist/css/bootstrap.min.css';
import './DropZone.css';
import './Buttons.css'

const DropZone = ({ handleUploadProgress, setUploadedFileName, showAlert, handleFileUploadSuccess, selectedFiles, setSelectedFiles, setShowToast }) => {

  const [fileUploaded, setFileUploaded] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);


  // Dzēšamais gabals
  // const handleFileRemove = (fileName) => {
  //   setSelectedFiles(prevSelectedFiles => prevSelectedFiles.filter(file => file.name !== fileName));
  // };


  const handleFileSelection = useCallback((acceptedFiles) => {
    const newFiles = acceptedFiles.filter(file => {
      const fileExtension = file.name.split('.').pop().toLowerCase();
      return fileExtension === 'csv'; // Only allow CSV files
    });
  
    if (newFiles.length < acceptedFiles.length) {
      // Some files were rejected because they are not CSV files
      const invalidFiles = acceptedFiles.filter(file => !newFiles.includes(file));
      showAlert('warning', `Tas nav CSV fails: ${invalidFiles.map(file => `"${file.name}"`).join(', ')}`);
    }
  
    const uniqueFiles = newFiles.filter(file => !selectedFiles.some(selectedFile => selectedFile.name === file.name));
    const duplicateFiles = newFiles.filter(file => selectedFiles.some(selectedFile => selectedFile.name === file.name));
  
    // console.log('Accepted Files:', acceptedFiles);
    // console.log('Unique Files:', uniqueFiles);
    // console.log('Duplicate Files:', duplicateFiles);
  
    if (duplicateFiles.length > 0) {
      showAlert('warning', `Dublikātus nepieņemam: ${duplicateFiles.map(file => `"${file.name}"`).join(', ')}`);
    }
  
    if (uniqueFiles.length > 0) {
      setSelectedFiles(prevSelectedFiles => [...prevSelectedFiles, ...uniqueFiles]);
      setShowToast(true); // Show the toast when valid files are dropped
    }
  
    // console.log('Selected Files in DropZone:', selectedFiles);
  }, [selectedFiles, showAlert, setSelectedFiles, setShowToast]);
  
 
  const fileInputRef = useRef(null);

  const handleSelectButtonClick = () => {
    // console.log('Button clicked!');
    fileInputRef.current.click();
  };

  const { acceptedFiles, getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: handleFileSelection,
    multiple: true,
  });

  return (
    <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''} ${fileUploaded ? 'uploaded' : ''}`}>
      <input {...getInputProps({ accept: '.csv' })} />
      {isDragActive ? (
        <p className="">Pievienojiet failus šeit...</p>
      ) : (
        <div className="">
          {fileUploaded ? (
            <>
              <i className=""></i>
            </>
          ) : (
            <div>
              <i className={fileUploaded ? '' : ''}></i>
              <p className="">
                Nomet savu failu šeit
              </p>
            </div>
          )}
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
  handleUploadProgress: PropTypes.func.isRequired,
  setUploadedFileName: PropTypes.func.isRequired,
  showAlert: PropTypes.func.isRequired,
  setSelectedFiles: PropTypes.func.isRequired, // Add the prop type for setSelectedFiles
  setShowToast: PropTypes.func.isRequired, // Add the prop type for setShowToast
};

export default DropZone;
