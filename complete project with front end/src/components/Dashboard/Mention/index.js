import React, { useEffect, useContext } from 'react'
import "./Mention.css"
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import Tooltipp from 'react-bootstrap/Tooltip'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger'
import { totalMentions } from "../../../context/actions/dashboard"
import { GlobalContext } from "../../../context/Provider"


const Index = () => {
    const { dashboardState } = useContext(GlobalContext);

    const data = dashboardState.mentionsData

    console.log("total Mentions data->", dashboardState.mentionsData)
    return <div className="card-width d-flex flex-column" style={{ width: 450, height: 250 }}>
        <OverlayTrigger
            placement={'right'}
            overlay={
                <Tooltipp style={{ opacity: 0.7 }} >
                    See the total number of mentions of your brand across various social media platforms over time.
        </Tooltipp>
            }
        >
            <div className="card-title text-left">Total Mentions </div>
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
                <defs>
                    <linearGradient id="colortotal" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#5E77FF" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#5E77FF" stopOpacity={0} />
                    </linearGradient>
                </defs>
                {/* <CartesianGrid strokeDasharray="5 5" /> */}
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="total" stroke="#5E77FF" fillOpacity={1} fill="url(#colortotal)" />
            </AreaChart>
        </ResponsiveContainer>
    </div >

}

export default Index