import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './CSVUploader.css'; // Create a CSS file for styling the uploader


const CSVUploader = () => {
    const [uploading, setUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [fileUploaded, setFileUploaded] = useState(false);
  
    const handleUploadProgress = (progress) => {
      setUploadProgress(progress);
    };
  
    const onDrop = async (acceptedFiles) => {
      try {
        setUploading(true);
        const formData = new FormData();
        formData.append('file', acceptedFiles[0]);
  
        await axios.post('http://localhost:3001/api/upload', formData, {
          onUploadProgress: (progressEvent) => {
            const progress = Math.round((progressEvent.loaded / progressEvent.total) * 100);
            handleUploadProgress(progress);
          },
        });
  
        handleUploadProgress(100);
        setFileUploaded(true);
      } catch (error) {
        console.error(error);
        alert('An error occurred while uploading the file.');
        handleUploadProgress(0);
        setFileUploaded(false);
      } finally {
        setUploading(false);
      }
    };
  
    const { getRootProps, getInputProps, isDragActive } = useDropzone({
      onDrop,
      accept: 'text/csv',
      disabled: fileUploaded,
      maxFiles: 1,
    });
  
    return (
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''} ${fileUploaded ? 'uploaded' : ''}`}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p className="mb-0">Drop your file here...</p>
        ) : (
          <div className="d-flex flex-column align-items-center justify-content-center">
            {fileUploaded ? (
              <i className="bi bi-check-circle-fill"></i>
            ) : (
              <i className="bi bi-cloud-arrow-up-fill"></i>
            )}
            <p className="mb-0 mt-2">
              {fileUploaded ? 'File uploaded!' : 'Drop your file here'}
            </p>
            <button className="btn btn-primary btn-grey mt-2" disabled={fileUploaded}>
              {fileUploaded ? 'Thank you' : 'Choose File'}
            </button>
          </div>
        )}
      </div>
    );
  };
  
  export default CSVUploader;
  