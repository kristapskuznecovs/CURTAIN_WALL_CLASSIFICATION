import React, { useCallback } from 'react';
import axios from 'axios';
import './Buttons.css';
import { sessionStore } from '../stores/storeSessions';
import { observer } from 'mobx-react';
import { alertStore } from '../stores/storeAlerts';


const ButtonUpload = observer(({ selectedFiles }) => {
  const sessionId = sessionStore.sessionId; // Get the sessionId value from sessionStore

  const handleUpload = useCallback(async (formData) => {
    try {
      const response = await axios.post(process.env.REACT_APP_API_URL+'/api/upload/'+JSON.stringify(sessionId), formData);
      if (response.status === 200) {
        await startProcessing(response.data.filename);
      } else {
        //send an error to the user
        alertStore.addAlert('File upload failed!');
      }
    } catch (error) {
      // Handle any errors that occurred during the API call
      alertStore.addAlert('An error occurred while uploading the file.', error);
    }
  },[sessionId]);

  const startProcessing = async (filename) => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL}/api/process/${filename}/${JSON.stringify(sessionId)}`);
      console.log('File processing response:', response.data);
    } catch (error) {
      // Handle any errors that occurred during the API call
      alertStore.addAlert('An error occurred while starting file processing.', error);
    }
  };

  const handleButtonClick = async () => {
    console.log('handleButtonClick called');
    try {
      // Upload all selected files
      for (const file of selectedFiles) {
        const formData = new FormData();
        formData.append('file', file);
        // Perform the upload action using the handleUpload function
        await handleUpload(formData);
      }
    } catch (error) {
      // Handle errors
      alertStore.addAlert('An error occurred during upload:', error);
    }
  };

  return (
    <button
      type="button"
      className="button"
      onClick={handleButtonClick}
    >
      Augšupielādēt
    </button>
  );
});

export default ButtonUpload;
