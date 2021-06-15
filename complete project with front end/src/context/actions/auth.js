import {
  LOADING,
  LOGIN_SUCCESS,
  LOGIN_ERROR,
} from "../../helpers/constants";
import History from "../../utils/history";
import { AuthAxios } from "../../helpers/AuthAxios"



export const login = ({ email, password }) => (dispatch) => {
  console.log(email, password)

  AuthAxios.post("/auth", JSON.stringify({
    username: email,
    password: password
  }))
    .then((res) => {
      console.log("response login", res)
      localStorage.setItem('token', res.data.access_token)
      dispatch({
        type: LOGIN_SUCCESS,
        payload: res.data,
      });
      History.push('/dashboard')
    })
    .catch((err) => {
      console.log("error", err)
      dispatch({
        type: LOGIN_ERROR,
        payload: err.response ? err.response.data : "COULD NOT CONNECT",
      });
    })
}

export const logout = () => {
  // console.log(email, password)
  window.localStorage.clear();
  History.push('/login')
  console.log("there??", localStorage.token)
}


export const signup = ({ email, brand, keywords, password }) => (dispatch) => {
  dispatch({
    type: LOADING,
  });
  console.log("signup", keywords.toString())

  AuthAxios.post("/signup", JSON.stringify({
    username: email,
    brand: brand,
    keywords: keywords.toString(),
    password: password,
  }))
    .then((res) => {
      console.log("succcesss bitccchh!!!", res)
      History.push('/login')
    })
    .catch((err) => {
      console.log("error!!!", err)
      dispatch({
        type: LOGIN_ERROR,
        payload: err.response ? err.response.data : "COULD NOT CONNECT",
      });
    })
}

