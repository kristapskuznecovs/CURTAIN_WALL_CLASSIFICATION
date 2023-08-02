import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ListDownload.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFileArrowDown } from '@fortawesome/free-solid-svg-icons';

const ListDownload = () => {
  const [fileList, setFileList] = useState([]);

  useEffect(() => {
    fetchFileList();
  }, []);

  const fetchFileList = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/download/filelist');
      const data = response.data;
      const fileListArray = data.file_list;
      setFileList(fileListArray);
      console.log('Updated fileList state:', fileListArray);
    } catch (error) {
      console.error('Error fetching file list:', error);
    }
  };

  const handleRefresh = () => {
    fetchFileList();
  };

  const handleDownload = (filename) => {
    // Replace 'default' with the appropriate folder name if needed
    window.location.href = `http://127.0.0.1:5000/api/download/output/${filename}`;
  };

  return (
    <>
      <div style={{ maxWidth: '800px', margin: '0 auto' }}>
        <div className="list-group">
          {fileList.map((filename) => (
            <div key={filename} className="list-group-item list-group-item-action d-flex align-items-center">
              <span>{filename}</span>
              <button className="btn btn-secondary ml-auto" onClick={() => handleDownload(filename)}>
                <FontAwesomeIcon icon={faFileArrowDown} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default ListDownload;
