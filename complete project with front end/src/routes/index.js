import React from 'react'
import { Route, Switch } from "react-router-dom";
import App from "../App";
import Login from "../components/Auth/Login"
import Home from "../components/Home"
import Dashboard from "../components/Dashboard"
import Signup from "../components/Auth/Signup"


const Routes = () => {
  // const profileData = JSON.parse(localStorage.getItem("profileData"));
  return (
    <App>
      <Switch>
        {/* {profileData && <Route exact path="/" component={HomePage} />}
          {!profileData && <Route exact path="/" render={() => { window.location.href = "hey/index.html" }} />} */}
        <Route exact path="/" component={Home} />
        <Route exact path="/login" component={Login} />
        <Route exact path="/signup" component={Signup} />
        <Route exact path="/dashboard" component={Dashboard} />
      </Switch>
    </App>
  );
};

export default Routes;
