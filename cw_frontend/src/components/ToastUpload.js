import React, { useRef, useEffect } from 'react';
import { Toast } from 'bootstrap';
import './ToastUpload.css';
import './Buttons.css';

const ToastUpload = ({ show, handleClose, fileName, progress }) => {
  const toastRef = useRef(null);

  useEffect(() => {
    if (show) {
      showToast();
    }
  }, [show]);

  const showToast = () => {
    const toastElement = toastRef.current;
    const toast = new Toast(toastElement, {
      autohide: false // Prevent the toast from automatically hiding
    });
    toast.show();
  };

const renderProgress = () => {
  if (progress === 100) {
    return (
      <div className="d-flex align-items-center">
        <div className="spinner-grow text-success toast-spinner me-2" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <span>{fileName}</span>
        <i className="bi bi-check-circle-fill text-success ms-2"></i>
      </div>
    );
  } else {
    return (
      <div className="d-flex align-items-center">
        <div className="spinner-border text-primary toast-spinner me-2" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <span>{fileName}</span>
        <span className="ms-2">Uploading: {progress}%</span>
      </div>
    );
  }
};

  return (
    <div>
      <div className="toast" ref={toastRef} role="alert" aria-live="assertive" aria-atomic="true">
        <div className="toast-header bg-light">
          <strong className="me-auto">Pievienotie faili </strong>
          <button type="button" className="btn-close" data-bs-dismiss="toast" aria-label="Close" onClick={handleClose}></button>
        </div>
        <div className="toast-body">
          {renderProgress()}
      </div>
    </div>
  </div>
  );
};

export default ToastUpload;
