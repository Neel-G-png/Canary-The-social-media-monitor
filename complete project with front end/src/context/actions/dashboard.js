import { AuthAxios } from "../../helpers/AuthAxios.js";
import AxiosInstance from "../../helpers/AxiosInstance.js"
import {
	OUTREACH_SUCCESS,
	ERROR,
	SENTIMENT_SUCCESS,
	BUZZ_SUCCESS,
	WORDLCLOUD_SUCCESS,
	MENTIONS_SUCCESS,
	GET_IDENTITY
} from "../../helpers/constants";


export const buzz = (user) => async (dispatch) => {
	// dispatch({
	//     type: LOADING,
	// });

	await AxiosInstance.get("/buzz", {
		params: {
			user
		}
	})
		.then((res) => {
			dispatch({
				type: BUZZ_SUCCESS,
				payload: res,
			});
			console.log("buzz data is here so now next")
			outreach(user)(dispatch)
		})
		.catch((err) => {
			console.log("error!!!", err)
			dispatch({
				type: ERROR,
				payload: err.response ? err.response.data : "COULD NOT CONNECT",
			});
		})
}

export const outreach = (user) => async (dispatch) => {
	// dispatch({
	//     type: LOADING,
	// });
	await AxiosInstance.get("/outreach", {
		params: {
			user
		}
	})
		.then((res) => {
			dispatch({
				type: OUTREACH_SUCCESS,
				payload: res,
			});
			console.log("outreach data is here so now next")
			sentiment(user)(dispatch)
			wordCloud(user)(dispatch)
			totalMentions(user)(dispatch)
		})
		.catch((err) => {
			console.log("error!!!", err)
			dispatch({
				type: ERROR,
				payload: err.response ? err.response.data : "COULD NOT CONNECT",
			});
		})
}

export const sentiment = (user) => async (dispatch) => {
	// dispatch({
	//     type: LOADING,
	// });

	await AxiosInstance.get("/sentiment", {
		params: {
			user
		}
	})
		.then((res) => {
			dispatch({
				type: SENTIMENT_SUCCESS,
				payload: res,
			})
			console.log("sentiment data is here so now next")
		})
		.catch((err) => {
			console.log("error!!!", err)
			dispatch({
				type: ERROR,
				payload: err.response ? err.response.data : "COULD NOT CONNECT",
			});
		})
}


export const wordCloud = (user) => async (dispatch) => {
	// dispatch({
	//     type: LOADING,
	// });
	await AxiosInstance.get("/wordcloud", {
		params: {
			user
		}
	})
		.then((res) => {
			dispatch({
				type: WORDLCLOUD_SUCCESS,
				payload: res,
			});

		})
		.catch((err) => {
			console.log("error!!!", err)
			dispatch({
				type: ERROR,
				payload: err.response ? err.response.data : "COULD NOT CONNECT",
			});
		})
}

export const totalMentions = (user) => async (dispatch) => {
	// dispatch({
	//     type: LOADING,
	// });
	await AxiosInstance.get("/totalMentions", {
		params: {
			user
		}
	})
		.then((res) => {
			dispatch({
				type: MENTIONS_SUCCESS,
				payload: res,
			});
		})
		.catch((err) => {
			console.log("error!!!", err)
			dispatch({
				type: ERROR,
				payload: err.response ? err.response.data : "COULD NOT CONNECT",
			});
		})
}

export const identity = (dispatch) => {
	AxiosInstance.get("/protected")
		.then((res) => {
			console.log("Identity found bitccchh!!!", res)
			localStorage.setItem('user', res.data)
			dispatch({
				type: GET_IDENTITY,
				payload: res,
			});

		})
		.catch((err) => {
			console.log("error!!!", err)
			dispatch({
				type: ERROR,
				payload: err.response ? err.response.data : "COULD NOT CONNECT",
			});
		})
}