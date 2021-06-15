import React, { useEffect, useContext } from 'react'
import ReactWordcloud from 'react-wordcloud';
import Tooltip from 'react-bootstrap/Tooltip'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger'
import { wordCloud } from "../../../context/actions/dashboard"
import { GlobalContext } from "../../../context/Provider"

const Index = () => {

    const { dashboardState } = useContext(GlobalContext);

    console.log("Word Cloud data->", dashboardState.buzzData)

    const words = dashboardState.wordCloudData
    return <div className="d-flex flex-column px-2">
        <OverlayTrigger
            placement={'right'}
            overlay={
                <Tooltip style={{ opacity: 0.7 }} >
                    See all the keywords related to your brand across various social media platforms
        </Tooltip>}
        >
            <div className="card-title text-left">Word Cloud</div>
        </OverlayTrigger>
        <div style={{ height: 250, width: 260 }}>
            <ReactWordcloud words={words} options={{
                fontFamily: 'Georgia, serif',
                fontSizes: [20, 50],
                colors: ['#5E77FF', '#A7B4FF', '#D5DBFD', '#C35BB1', '#6B64F7', '#be8e96']
            }} />
        </div>
    </div>
}

export default Index