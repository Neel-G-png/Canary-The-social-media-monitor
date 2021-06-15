import React from 'react'
import "./Dashboard.css"
import Buzz from "./Buzz"
import Sentiment from "./Sentiment"
import WordCloud from "./WordCloud"
import Mention from "./Mention"
import Predictor from "./Predictor"
import { useContext, useEffect } from 'react';
import { GlobalContext } from "../../context/Provider"
import Socket from "../../Socket"
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import Loader from "react-loader-spinner";
import { outreach, totalMentions, buzz, sentiment, wordCloud, identity } from '../../context/actions/dashboard'
import TestAxios from "../test/TestAxios"


const Dashboard = () => {
  const { time, dashboardDispatch, dashboardState } = useContext(GlobalContext)

  useEffect(() => {
    identity(dashboardDispatch)
  }, [])

  useEffect(() => {
    async function getData() {
      await buzz(dashboardState.identity)(dashboardDispatch)
    }
    getData()

  }, [dashboardState.identity])

  return <div className="dashboard-body">
    {/* <div>Time : {time}</div> */}
    {(dashboardState.outreachData.length !== 0 && dashboardState.sentimentData.line.length !== 0 &&
      dashboardState.sentimentData.pie.length !== 0 && dashboardState.buzzData.length !== 0 &&
      dashboardState.wordCloudData.length !== 0 && dashboardState.mentionsData.length !== 0)
      ? (<div data-testid="show-data">
        <div className="card-bodyTop" >
          <p id="some-id"></p>
          <div className="card m-2 p-3 body-radius  one" data-testid="outreach">
            <Predictor />
          </div>
          <div className="card m-2 p-3 body-radius two">
            <Sentiment />
          </div>
        </div>
        <div className="card-bodyTop">
          <div className="card m-2 p-3 body-radius three">
            <Buzz />
          </div>
          <div className="card m-2 p-3 body-radius five">
            <WordCloud />
          </div>
          <div className="card m-2 p-3 body-radius four ">
            <Mention />
          </div>
        </div>
      </div>
      ) :
      <div className="loaderDiv">
        <div className="loadingImg">
          <Loader
            type="Grid"
            color="#7B67F2"
            height={150}
            width={250}
          /></div>
        <div className="loadText mt-6" data-testid="loader"> Updating the Dashboard</div>
      </div>}

    {/* <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div><div>Icons made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div> */}
  </div>

  // return <TestAxios />
}

export default Dashboard