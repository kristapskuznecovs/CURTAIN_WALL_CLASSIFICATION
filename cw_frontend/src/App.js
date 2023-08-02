import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css';
import ClassificationPage from './pages/ClassificationPage';
import AboutPage from './pages/AboutPage';
import NavBar from './components/NavBar';
import Alert from './components/Alert';
import { v4 as uuidv4 } from 'uuid';
import './App.css';

const App = () => {
  const [alert, setAlert] = useState(null); // Alert state
  const [, setSessionId] = useState(null); // Session ID state

  // Function to display an alert
  const showAlert = (type, message) => {
    setAlert({ type, message });
  };

  // Function to hide the alert
  const hideAlert = () => {
    setAlert(null);
  };

// Generate or retrieve the session ID from local storage
useEffect(() => {
  let sessionId = localStorage.getItem('session_id');
  let storedDate = localStorage.getItem('session_date');
  let currentDate = new Date().toLocaleDateString();
  if (!sessionId || storedDate !== currentDate) {
    sessionId = uuidv4();
    localStorage.setItem('session_id', sessionId);
    localStorage.setItem('session_date', currentDate);
  }
  setSessionId(sessionId);
}, []);


  return (
    <Router>
      <div className="app-container">
        <NavBar />
        <div className="page-container">
          {alert && ( // Render the alert if it exists
            <Alert type={alert.type} message={alert.message} onClose={hideAlert} />
          )}
          <Routes>
            <Route
              path="/"
              element={
                <div className="page-container">
                  <ClassificationPage showAlert={showAlert} />
                </div>
              }
            />
            <Route
              path="/classification"
              element={
                <div className="page-container">
                  <ClassificationPage showAlert={showAlert} />
                </div>
              }
            />
            <Route
              path="/about"
              element={
                <div className="page-container">
                  <AboutPage />
                </div>
              }
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
