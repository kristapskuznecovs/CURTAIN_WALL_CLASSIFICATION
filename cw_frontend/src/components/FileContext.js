import React, { createContext, useState, useContext } from 'react';

const FileContext = createContext();

export const FileProvider = ({ children }) => {
  const [files, setFiles] = useState([]);

  const addFile = (file) => {
    setFiles([...files, { ...file, state: 'selected' }]);
  };

  const updateFileState = (fileName, state) => {
    setFiles(
      files.map((file) => {
        if (file.name === fileName) {
          return { ...file, state };
        }
        return file;
      })
    );
  };

  const markFileAsSelected = (fileName) => {
    updateFileState(fileName, 'selected');
  };

  const markFileAsUploading = (fileName) => {
    updateFileState(fileName, 'uploading');
  };

  const markFileAsUploaded = (fileName) => {
    updateFileState(fileName, 'uploaded');
  };

  const markFileAsAnalyzing = (fileName) => {
    updateFileState(fileName, 'analysing');
  };

  const markFileAsAnalysed = (fileName) => {
    updateFileState(fileName, 'analysed');
  };

  const markFileAsDownloading = (fileName) => {
    updateFileState(fileName, 'downloading');
  };

  const markFileAsDownloaded = (fileName) => {
    updateFileState(fileName, 'downloaded');
  };

  return (
    <FileContext.Provider
      value={{
        files,
        addFile,
        updateFileState,
        markFileAsSelected,
        markFileAsUploading,
        markFileAsUploaded,
        markFileAsAnalyzing,
        markFileAsAnalysed,
        markFileAsDownloading,
        markFileAsDownloaded
      }}
    >
      {children}
    </FileContext.Provider>
  );
};

export const useFileState = () => useContext(FileContext);
