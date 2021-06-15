import './App.css';
import NavSlide from './components/NavSlide'
import { withRouter } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import isAuthenticated from "./utils/isAuthenticated"


function App(props) {

  return (
    <div className="App">
      {props.location.pathname === "/login" || props.location.pathname === "/" ||
        props.location.pathname === "/signup" ? (
        <div className=" signin-container ">
          {/* <div style={{ background: "linear-gradient(90deg, rgba(141,208,244,1) 37%, rgba(255,126,159,1) 94%)", height: 10 }}></div> */}
          {props.children}
        </div>
      ) : (
        <div>
          {isAuthenticated() ? (<div> <NavSlide />
            {props.children}</div>) : props.history.push("/login")}
        </div>
      )}
      {/* <div className="home-footer"><a style={{ color: "#4a4a4a" }} href="https://github.com/RiyaNegi/Social-Monitoring">A project made with ❤️ by Riya Negi, Neel Gandhi  |  View source code</a></div> */}

    </div>
  );
}

export default withRouter(App);
