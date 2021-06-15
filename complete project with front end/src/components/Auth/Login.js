import React from 'react'
import "./Auth.css"
import SignImg from "../../assets/SignImg.png"
import { Form, Button } from "react-bootstrap"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faLock } from "@fortawesome/free-solid-svg-icons";
import { Link } from "react-router-dom";
import { useEffect, useState, useContext } from "react"
import { GlobalContext } from "../../context/Provider"
import { login } from "../../context/actions/auth";
import wave from "../../assets/wave3.png"
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';



const Login = () => {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 1200);
  const [form, setForm] = useState({
    email: "",
    password: ""
  })

  const notify = (warning) => toast.error(warning, {
    position: "top-center",
    autoClose: 3000,
    hideProgressBar: true,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
  });

  const { authDispatch, authState } = useContext(GlobalContext);

  useEffect(() => {
    window.addEventListener("resize", () => {
      const ismobile = window.innerWidth < 1200;
      if (ismobile !== isMobile) setIsMobile(ismobile);
    }, false);
  }, [isMobile]);

  useEffect(() => {
    if (authState.error) {
      notify(authState.error)
    }
  }, [authState.error])

  const onChange = (e) => {
    authState.error = ""
    setForm({
      ...form,
      [e.target.name]: e.target.value
    })
  }

  const submit = (e) => {
    e.preventDefault();
    login(form)(authDispatch);
  }


  return <div className="form-div">
    <div className="wave"><img src={wave} style={{ width: 1550, height: 790 }} /></div>
    <div className="form-card">
      <div className="form-title">Social Sprout</div>
      <hr className="container mt-2" style={{ outline: "none", border: "none", backgroundColor: "black", height: 0.5, width: "50%" }} />
      <div className="d-flex mt-5">
        {!isMobile && <div><img src={SignImg} style={{ width: 450, height: 350 }} /></div>}
        <div className="form-info" style={isMobile ? { marginLeft: 0 } : { marginLeft: 50 }}>
          <div className="form-header">Log In</div>
          <div className="form-values mt-5">
            <form className="d-flex flex-column">
              <div className="form-input">
                <FontAwesomeIcon icon={faUser} size="1x" color="black" />
                <input className="form-in ml-4" type="email" data-testid="email" placeholder="Enter Email-id" name="email" value={form.email} onChange={(e) => onChange(e)} />
              </div>
              <div className="form-input mt-5" >
                <FontAwesomeIcon icon={faLock} size="1x" color="black" />
                <input className="form-in ml-4" type="password" data-testid="password" placeholder="Enter Password" name="password" value={form.password} onChange={(e) => onChange(e)} />
              </div>
              <div className="form-btn">
                { }
                <button className="form-login mt-5 p-2" disabled={!form.email || !form.password} style={{ backgroundColor: !form.email || !form.password ? "#2d2d2d" : "black" }} onClick={(e) => submit(e)} >Login</button>
                {/* </Link> */}
                <div data-testid="warning">
                  <ToastContainer
                    position="top-center"
                    autoClose={3000}
                    hideProgressBar
                    newestOnTop={false}
                    closeOnClick
                    rtl={false}
                    pauseOnFocusLoss
                    draggable
                    pauseOnHover
                  />
                </div>
              </div>
            </form>
            <div className="mt-4 form-link">
              <Link style={{ color: "black", textDecoration: "underline" }} to="/signup">Don't have an account? Click here to create one!</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
}

export default Login