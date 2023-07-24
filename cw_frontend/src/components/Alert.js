import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import './Alert.css';

const Alert = ({ type, message, onClose }) => {
  const [show, setShow] = useState(false);

  useEffect(() => {
    // Show the alert after a small delay to trigger the transition effect
    const timer = setTimeout(() => {
      setShow(true);
    }, 100);

    // Clean up the timer on component unmount
    return () => {
      clearTimeout(timer);
    };
  }, []);

  return (
    <div className={`alert alert-${type} ${show ? 'show' : ''}`} role="alert">
      <div className="d-flex align-items-center">
    <div className="flex-grow-1">{message}</div>
    <button type="button" className="btn-close ms-3" aria-label="Close" onClick={onClose}></button>
  </div>
</div>
  );
};
  
Alert.propTypes = {
  type: PropTypes.string.isRequired,
  message: PropTypes.string.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default Alert;
