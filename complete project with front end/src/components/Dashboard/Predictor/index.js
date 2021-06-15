import React, { useEffect, useContext } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import Tooltipp from 'react-bootstrap/Tooltip'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger'
import { outreach } from "../../../context/actions/dashboard"
import { GlobalContext } from "../../../context/Provider"


const Predictor = () => {
    const { dashboardState } = useContext(GlobalContext);

    console.log("outreach data->", dashboardState)


    const data = dashboardState.outreachData

    return <div style={{ width: 700, height: 260 }}>
        <OverlayTrigger
            placement={'right'}
            overlay={
                <Tooltipp style={{ opacity: 0.7 }} >
                    See how much outreach your brand is getting across various social media platforms
        </Tooltipp>
            }
        >
            <div className="card-title text-left">Outreach Predictor</div>
        </OverlayTrigger>
        < ResponsiveContainer width="100%" height="100%">
            <AreaChart
                width={200}
                height={150}
                data={data}
                margin={{
                    top: 10,
                    right: 30,
                    left: 0,
                    bottom: 0,
                }}
            >
                {/* <defs>
                    <linearGradient id="colorlow" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#E25960" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#E25960" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="colorhigh" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#323232" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#323232" stopOpacity={0} />
                    </linearGradient>
                </defs> */}
                <XAxis dataKey="date" />
                {/* <CartesianGrid strokeDasharray="5 5" /> */}
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="low" stroke="#5E77FF" fill="#5E77FF" />
                <Area type="monotone" dataKey="high" stroke="#C989EB" fill="#C989EB" />
            </AreaChart>
        </ResponsiveContainer>
    </div>
}

export default Predictor

