import React, { useState } from 'react';
import styled from 'styled-components';
import Heading from '../components/Heading';
import PageLayout from '../components/PageLayout';
import DropZone from '../components/DropZone';
import ToastUpload from '../components/ToastUpload';
import ButtonUpload from '../components/ButtonUpload';
import ButtonDownload from '../components/ButtonDownload';
import ListDownload from '../components/ListDownload';
import './Text.css'

const DropZoneContainer = styled.div`
margin-top: 16px;  
margin-bottom: 16px;
/*border: 1px solid #ccc;*/
`;

const ButtonContainer = styled.div`
margin-top: 16px  
margin-bottom: 16px;
display: flex;
  justify-content: space-between;
  align-items: center;
  /*border: 1px solid #ccc;*/
`;

const ListContainer = styled.div`
margin-top: 16px  
margin-bottom: 16px;
/*border: 1px solid #ccc;*/
`;

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

  const handleCloseToast = () => {
    setShowToast(false);
  };

  const handleFileRemove = (fileName) => {
    setSelectedFiles(prevSelectedFiles => prevSelectedFiles.filter(file => file.name !== fileName));
  };

  return (
    <PageLayout>
        <Heading>Pievieno fasādes failu</Heading>
        <DropZoneContainer>
          <DropZone
            handleUploadProgress={handleUploadProgress}
            setUploadedFileName={setUploadedFileName}
            showAlert={showAlert}
            handleFileUploadSuccess={handleFileUploadSuccess}
            selectedFiles={selectedFiles}
            setSelectedFiles={setSelectedFiles}
            setShowToast={setShowToast}
          />
        </DropZoneContainer>
        <ButtonContainer>
          <ButtonUpload
            fileName={uploadedFileName}
            handleFileUploadSuccess={handleFileUploadSuccess}
            selectedFiles={selectedFiles}
          />
          <ButtonDownload/>
        </ButtonContainer>
        <ListContainer>
        <Heading>Failu saraksts</Heading>
        <ListDownload />
        </ListContainer>
        {showToast && (
          <ToastUpload
            show={showToast}
            handleClose={handleCloseToast}
            fileName={uploadedFileName}
            progress={uploadProgress}
            selectedFiles={selectedFiles}
            handleFileRemove={handleFileRemove}
          />
        )}
    </PageLayout>

  );
};

export default ClassificationPage;