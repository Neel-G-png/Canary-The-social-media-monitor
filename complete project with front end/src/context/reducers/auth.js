import {
  REGISTER_LOADING,
  REGISTER_SUCCESS,
  REGISTER_ERROR,
  LOADING,
  LOGIN_SUCCESS,
  LOGIN_ERROR,
} from "../../helpers/constants";

const auth = (state, { payload, type }) => {
  switch (type) {
    case REGISTER_LOADING:
    case LOADING:
      return {
        ...state,
        auth: {
          ...state.auth,
          error: false,
          loading: true,
        },
      };

    case REGISTER_SUCCESS:
    case LOGIN_SUCCESS:
      return {
        ...state,
        auth: {
          ...state.auth,
          loading: false,
          data: payload,
          loggedIn: true
        },
      };

    case LOGIN_ERROR:
      console.log("hey caleed@@")
      return {
        ...state,
        error: "Login failed. Wrong email or password",
      };
    default:
      return state;
  }
};

export default auth;