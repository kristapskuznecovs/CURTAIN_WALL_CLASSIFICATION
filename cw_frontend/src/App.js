import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css';
import ClassificationPage from './pages/ClassificationPage';
import AboutPage from './pages/AboutPage';
import NavBar from './components/NavBar';
import Alert from './components/Alert';
import './App.css';

const App = () => {
  const [alert, setAlert] = useState(null); // Alert state

  // Function to display an alert
  const showAlert = (type, message) => {
    setAlert({ type, message });
  };

  // Function to hide the alert
  const hideAlert = () => {
    setAlert(null);
  };

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
