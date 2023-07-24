import React from 'react';
import axios from 'axios';
import './Buttons.css';

const ButtonDownload = () => {
  const handleDownload = async () => {
    try {
      const response = await axios({
        url: 'http://localhost:5000/api/download/output_grouping.csv', // Replace with the actual endpoint URL
        method: 'GET',
        responseType: 'blob', // Important for downloading files
        params: {
          filename: 'output_grouping.csv', // Set the desired filename here
        },
      });

      const href = URL.createObjectURL(response.data);

      const link = document.createElement('a');
      link.href = href;
      link.setAttribute('download', 'React.txt'); // Set the desired filename and extension
      document.body.appendChild(link);
      link.click();

      document.body.removeChild(link);
      URL.revokeObjectURL(href);
    } catch (error) {
      console.error(error);
      alert('An error occurred while downloading the file.');
    }
  };

  return (
    <div>
      <button className="button" onClick={handleDownload}>
        Download
      </button>
    </div>
  );
};

export default ButtonDownload;
