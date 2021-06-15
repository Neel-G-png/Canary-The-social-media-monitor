import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';


const Linegraph = (lineData) => {
    console.log("line data", lineData.lineData)
    const data = lineData.lineData
    return <ResponsiveContainer width="100%" height="100%">
        <LineChart
            width={300}
            height={300}
            data={data}
            margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
            }}
        >
            {/* <CartesianGrid strokeDasharray="3 3" /> */}
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="negative" stroke="#6B64F7" activeDot={{ r: 8 }} />
            <Line type="monotone" dataKey="positive" stroke="#C35BB1" />
        </LineChart>
    </ResponsiveContainer>
}

export default Linegraph

