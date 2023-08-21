import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css';
import ClassificationPage from './pages/ClassificationPage';
import AboutPage from './pages/AboutPage';
import NavBar from './components/NavBar';
import Alert from './components/Alert';
import ListDownload from './components/ListDownload';
import { observer } from 'mobx-react';
import { sessionStore } from './stores/storeSessions';
import { alertStore } from './stores/storeAlerts';
import './App.css';

const App = observer(() => {
  const { sessionId } = sessionStore;
  const [alert, setAlert] = useState(null);

  // Function to display an alert
  const showAlert = (type, message) => {
    setAlert({ type, message });
  };

  // Function to hide the alert
  const hideAlert = () => {
    setAlert(null);
  };

sessionStore.generateSessionId();
console.log('Session ID:', sessionId);

return (
    <Router>
      <div className="app-container">
        <NavBar />
        <div className="page-container">
        {alertStore.alerts.map((alert, index) => (
            <Alert key={index} type={alert.type} message={alert.message} onClose={() => alertStore.hideAlertAlert(index)} />
          ))}
          {alert && ( // Render the current alert if it exists
            <Alert type={alert.type} message={alert.message} onClose={hideAlert} />
          )}
          <Routes>
            <Route
              path="/"
              element={
                <div className="page-container">
                  <ClassificationPage showAlert={showAlert} />
                  <ListDownload sessionId={sessionId} />
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
});

export default App;
