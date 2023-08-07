import React, { useRef, useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleStop, faTrashCan, faChevronUp, faChevronDown } from '@fortawesome/free-solid-svg-icons';

import './ToastUpload.css';

const ToastUpload = ({ show, progress, selectedFiles, handleFileRemove }) => {
  const [isMinimized, setIsMinimized] = useState(false);
  const [shouldShow, setShouldShow] = useState(show);
  const toastRef = useRef(null);

  useEffect(() => {
    // Update the shouldShow state based on the selectedFiles length
    setShouldShow(selectedFiles.length > 0);
  }, [selectedFiles]);

  const handleMinimize = () => {
    setIsMinimized(true);
  };

  const handleMaximize = () => {
    setIsMinimized(false);
  };

  const renderFilesList = () => {
    return (
      <div>
        <ul style={{ listStyleType: "none", padding: 0 }}>
          {selectedFiles.map((file, index) => (
            <li key={index} style={{ display: "flex", alignItems: "center" }}>
              <span style={{ marginRight: "8px" }}>
                <FontAwesomeIcon icon={faCircleStop} style={{ color: progress === 100 ? 'green' : 'grey' }} />
                </span>
                <span style={{ flex: 1, overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis" }}>
                {file.name}
                </span>
              <button onClick={() => handleFileRemove(file.name)} className="trash-button">
                <FontAwesomeIcon icon={faTrashCan} />
              </button>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  return (
      <div>
        <div className={`toast ${shouldShow ? 'show' : ''} ${isMinimized ? 'minimized' : ''}`} ref={toastRef} role="alert" aria-live="assertive" aria-atomic="true">
        <div className="toast-header bg-light">
        <strong className="me-auto">Pievienoti {selectedFiles.length} faili </strong>
          <div className="button-group">
            <button type="button" className="min-max-button" onClick={isMinimized ? handleMaximize : handleMinimize}>
              <FontAwesomeIcon icon={isMinimized ? faChevronUp : faChevronDown} />
            </button>
          </div>
        </div>
        {!isMinimized && (
          <div className="toast-body">
            {renderFilesList()}
          </div>
        )}
      </div>
    </div>
  );
};

export default ToastUpload;
