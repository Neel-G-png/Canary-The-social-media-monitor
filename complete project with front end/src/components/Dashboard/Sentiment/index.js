import React, { useEffect, useContext } from 'react'
import Sentiment from "./Sentiment"
import Line from "./Line"
import Tooltip from 'react-bootstrap/Tooltip'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger'
import { sentiment } from "../../../context/actions/dashboard"
import { GlobalContext } from "../../../context/Provider"
import Legend from "./Legend.js"


const Index = () => {

    const { dashboardState } = useContext(GlobalContext);

    return <div className="d-flex flex-column px-3" >
        <OverlayTrigger
            placement={'right'}
            overlay={
                <Tooltip style={{ opacity: 0.7 }} >
                    See the sentiments of all the mentions of your brand across various social media platforms and how the audience is receiving it
                 </Tooltip>}
        >
            <div className="card-title text-left">Sentiment Analysis</div>
        </OverlayTrigger>
        <div className="d-flex">
            <div style={{ width: 200, height: 200 }}>
                {/* <Legend /> */}
                <Sentiment pieData={dashboardState.sentimentData.pie} />
            </div>
            <div style={{ width: 470, height: 260 }}>
                <Line lineData={dashboardState.sentimentData.line} />
            </div>
        </div>

    </div >
}

export default Index