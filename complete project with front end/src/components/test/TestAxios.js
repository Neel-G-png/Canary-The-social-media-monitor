import React from 'react'
import axios from 'axios'
import AxiosInstance from "../../helpers/AxiosInstance"

const TestAxios = ({ url }) => {
    const [data, setData] = React.useState()

    const fetchData = async () => {
        const response = await AxiosInstance.get(url).then(() => { console.log("onsode thennn!!@!@!@") })
        setData(response.data.greeting)
    }

    return (
        <>
            <button onClick={fetchData} data-testid="fetch-data">Load Data</button>
            {
                data ?
                    <div data-testid="show-data">{data}</div> :
                    <h1 data-testid="loading">Loading...</h1>
            }
        </>
    )
}

export default TestAxios