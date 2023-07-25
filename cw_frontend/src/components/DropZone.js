import React, { useCallback, useState } from 'react';
import PropTypes from 'prop-types';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './DropZone.css';
import './Buttons.css';

const DropZone = ({ handleUploadProgress, setUploadedFileName, showAlert, handleFileUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [fileUploaded, setFileUploaded] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const handleFileUpload = useCallback(async (acceptedFiles) => {
    try {
      if (acceptedFiles.length === 0) {
        // No files were dropped, handle the situation accordingly
        return;
      }
      console.log('Accepted Files:', acceptedFiles);

      const newFiles = acceptedFiles.filter(file => {
        const fileExtension = file.name.split('.').pop().toLowerCase();
        return fileExtension === 'csv'; // Only allow CSV files
      });
  
      if (newFiles.length === 0) {
        // Handle the case when no valid files are dropped
        showAlert('warning', 'Augšupielādēt var tikai .csv failus!');
        return;
      }
  
      setUploading(true);

      const formData = new FormData();
      newFiles.forEach(file => {
        formData.append('file', file); // Append each file to the FormData
      });
      console.log('FormData:', formData);

      setFileUploaded(true);
      setUploadedFiles(prevUploadedFiles => [...prevUploadedFiles, ...newFiles]);
      newFiles.forEach(file => {
        handleFileUploadSuccess(file.name);
      });
      
      await uploadFile(formData);

    } catch (error) {
      console.error('An error occurred while uploading the file.', error);
      showAlert('danger', 'Augšupielādējot failu, ir notikusi kļūda!');
      handleUploadProgress(0);
      setFileUploaded(false);

    } finally {
      setUploading(false);
    }
  }, [handleUploadProgress, showAlert, handleFileUploadSuccess]);


  const uploadFile = async (formData) => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/upload', formData, {
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
          handleUploadProgress(progress);
        },
      });
  
      // Check the response status to determine if the upload was successful
      if (response.status === 200) {
        // Handle the case of successful file upload
        handleFileUploadSuccess(response.data.fileName);
        showAlert('success', 'Fails augšupielādēts veiksmīgi!');
      } else {
        // Handle the case of unsuccessful file upload (show error message)
        showAlert('danger', 'Augšupielādējot failu, ir notikusi kļūda!');
      }
    } catch (error) {
      // Handle any errors that occurred during the API call (show error message)
      showAlert('danger', 'Augšupielādējot failu, ir notikusi kļūda!');
      console.error('An error occurred while uploading the file.', error);
    }
  };
  
 

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: handleFileUpload,
    disabled: fileUploaded || uploadedFiles.length >= 3,
    multiple: true, // Allow multiple files to be dropped
    maxFiles: 3, // Limit the maximum number of files to 3
  });

  return (
    <div
      {...getRootProps()}
      className={`dropzone ${isDragActive ? 'active' : ''} ${fileUploaded ? 'uploaded' : ''}`}
    >
      <input {...getInputProps({ accept: '.csv' })} />
      {isDragActive ? (
        <p className="mb-0">Pievienojiet fails šeit...</p>
      ) : (
        <div className="d-flex flex-column align-items-center justify-content-center">
          {fileUploaded ? (
            <i className="bi bi-check-circle-fill"></i>
          ) : (
            <i className="bi bi-cloud-arrow-up-fill"></i>
          )}
          <p className="mb-0 mt-12">
            {fileUploaded ? 'Fails augšupielādēts!' : 'Nomet savu failu šeit'}
          </p>
          <button className="button" disabled={fileUploaded || uploadedFiles.length >= 3}>
            {fileUploaded ? 'Paldies' : 'Izvēlies failu'}
          </button>
        </div>
      )}
    </div>
  );
};

DropZone.propTypes = {
  handleUploadProgress: PropTypes.func.isRequired,
  setUploadedFileName: PropTypes.func.isRequired,
  showAlert: PropTypes.func.isRequired,
};

export default DropZone;
