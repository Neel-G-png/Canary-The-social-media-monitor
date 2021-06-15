import React from 'react'
import { PieChart, Pie, Sector, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import Legend from "./Legend";

const COLORS = ['#8495F5', '#A7B4FF', '#C6CFFE', '#D5DBFD', '#5E77FF'];

const RADIAN = Math.PI / 180;

const Sentiment = (pieData) => {
    console.log("Pie data", pieData.pieData)
    const data = pieData.pieData
    const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, index }) => {
        const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
        const x = cx + radius * Math.cos(-midAngle * RADIAN);
        const y = cy + radius * Math.sin(-midAngle * RADIAN);

        return (
            <text
                x={x}
                y={y}
                fill="white"
                textAnchor="middle"
            >
                {`${(percent * 100).toFixed(0)}%`}
            </text>
        );
    };

    return (
        < ResponsiveContainer width="100%" height="100%">
            <PieChart width={70} height={30}>
                <Legend verticalAlign="top" height={20} />
                <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={renderCustomizedLabel}
                    outerRadius={90}
                    nameKey="name" valueKey="value"
                    fill="#8884d8"
                    dataKey="value"
                >
                    {data.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                    <Tooltip />
                </Pie>
            </PieChart>
        </ResponsiveContainer>
    )

}

export default Sentiment