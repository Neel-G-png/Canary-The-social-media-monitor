import React, { useEffect, useContext } from 'react'
import { GlobalContext } from "../../../context/Provider"
import "./sentiment.css"

const Legend = () => {
    const { dashboardState } = useContext(GlobalContext);
    const data = dashboardState.sentimentData.pie

    const Colors = ["#5E77FF", "#8495F5", "#A7B4FF", "#C6CFFE", "#D5DBFD"];

    return (
        <div className="legend">
            {data.map((index, key) => (<div className="ml-2">
                <div className="legendColor" style={{ backgroundColor: Colors[key] }}></div>
                <div className="legendName">{index.name}</div></div>))}
        </div>
    )
}

export default Legend