import {
  OUTREACH_SUCCESS,
  ERROR,
  SENTIMENT_SUCCESS,
  BUZZ_SUCCESS,
  WORDLCLOUD_SUCCESS,
  MENTIONS_SUCCESS,
  LOADING,
  GET_IDENTITY
} from "../../helpers/constants";

const dashboard = (state, { payload, type }) => {
  switch (type) {
    case OUTREACH_SUCCESS:
      console.log("outreach payload->", payload.data)
      return {
        ...state,
        outreachData: payload.data.highlow,
        isloading: false
      }
    case SENTIMENT_SUCCESS:
      return {
        ...state,
        sentimentData: {
          line: payload.data.line,
          pie: payload.data.pie,
          isloading: false
        }
      }
    case BUZZ_SUCCESS:
      return {
        ...state,
        buzzData: payload.data,
        isloading: false
      }
    case WORDLCLOUD_SUCCESS:
      return {
        ...state,
        wordCloudData: payload.data.wordcloud,
        isloading: false
      }
    case MENTIONS_SUCCESS:
      return {
        ...state,
        mentionsData: payload.data.total_mentions,
        isloading: false
      }
    case GET_IDENTITY:
      return {
        ...state,
        identity: payload.data,
        isloading: false
      }
    case LOADING:
      console.log("LOADING DATA!:", state)
      return {
        ...state,
        isloading: true
      }
    case ERROR:
      return {
        ...state
      }
    default:
      return state;
  }
};

export default dashboard;