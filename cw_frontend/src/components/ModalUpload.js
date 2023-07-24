import React from 'react';
import PropTypes from 'prop-types';
import { Modal, Button } from 'react-bootstrap';
import './ModalUpload.css';

const ModalUpload = ({ show, handleClose, fileName, progress }) => {
  return (
    <Modal show={show} onHide={handleClose} className="modal-upload">
      <Modal.Header closeButton>
        <Modal.Title>Upload Progress</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p>File: {fileName}</p>
        <p>Progress: {progress}%</p>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={handleClose}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

ModalUpload.propTypes = {
  show: PropTypes.bool.isRequired,
  handleClose: PropTypes.func.isRequired,
  fileName: PropTypes.string.isRequired,
  progress: PropTypes.number.isRequired,
};

export default ModalUpload;
