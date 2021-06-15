import React from "react";
import { Navbar, Nav } from "react-bootstrap";
import { Link } from "react-router-dom"
import "./Style.css"
import { logout } from "../context/actions/auth";


const NavSlide = () => {
  const handleLogout = () => {
    logout()
  }
  return <div>
    <Navbar className="px-4 py-1" bg="dark" variant="dark">
      <Navbar.Brand className="web-name" href="/dashboard"><div className="mt-1">Social Sprout</div></Navbar.Brand>
      <Nav className="ml-auto">
        <div className="link mr-4" onClick={() => handleLogout()}>Logout</div>
        <div className="link" onClick={() => handleLogout()}>Profile</div>
      </Nav>
    </Navbar>
    <div style={{ background: "linear-gradient(128deg, rgba(86,102,254,1) 26%, rgba(222,107,207,1) 54%)", height: 5 }}></div>
  </div>
}

export default NavSlide