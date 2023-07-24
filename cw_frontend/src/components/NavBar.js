import React from 'react';
import { NavLink } from 'react-router-dom';
import './NavBar.css';
import logo from '../assets/logo.svg';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';

const NavBar = () => {
  return (
    <Navbar bg="body-tertiary" expand="lg">
      <div className="container">
        <NavLink to="/" className="logo">
          <img src={logo} alt="Logo" width="300" height="30" className="d-inline-block align-text-top" />
        </NavLink>
        <Navbar.Toggle aria-controls="navbar-nav" />
        <Navbar.Collapse id="navbar-nav">
          <Nav className="ml-auto">
            <Nav.Item>
              <NavLink to="/classification" className="nav-link" activeclassname="active">
                KLASIFIKĀCIJA
                <div className="underline"></div>
              </NavLink>
            </Nav.Item>
            <Nav.Item>
              <NavLink to="/about" className="nav-link" activeclassname="active">
                PAR PROJEKTU
                <div className="underline"></div>
              </NavLink>
            </Nav.Item>
          </Nav>
        </Navbar.Collapse>
      </div>
    </Navbar>
  );
};

export default NavBar;
