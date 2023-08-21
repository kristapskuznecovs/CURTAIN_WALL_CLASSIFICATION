import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ListDownload.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFileArrowDown } from '@fortawesome/free-solid-svg-icons';

const ListDownload = ({ sessionId }) => {
  const [fileList, setFileList] = useState([]);

  useEffect(() => {
    fetchFileList();
  }, []);

  const fetchFileList = async () => {
    try {
      const response = await axios.get(process.env.REACT_APP_API_URL+'/api/download/filelist/'+JSON.stringify(sessionId));
      const data = response.data;
      // Check if data has the expected structure
      if (data.hasOwnProperty('file_list') && Array.isArray(data.file_list)) {
        setFileList(data.file_list);
      } else {
        // Set a default empty list if the structure is not as expected
        setFileList([]);
      }
    } catch (error) {
    }
  };
 

  const handleRefresh = () => {
    fetchFileList();
  };

  const handleDownload = (filename) => {
    const apiRoute = process.env.API_ROUTE;
    window.location.href = `${apiRoute}/api/download/output/${filename}`;
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
