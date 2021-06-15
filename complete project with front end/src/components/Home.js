import React from 'react'
import "./Style.css"

const Home = () => {
    return (
        <div className="homepage">
            <div className="home-nav">
                <div className="home-name ml-6 mt-3">Social Sprout </div>
                <div className="home-login "><a style={{ textDecoration: "none", color: "rgb(49, 49, 49)" }} href="/login">login</a></div>
            </div>
            <hr className="container" style={{ outline: "none", border: "none", backgroundColor: "black", height: 0.5, width: "80%" }} />

            <div className="home-text mt-5">Analyse and Understand how the internet perceives your brand. <br />Create the best possible persona for your brand on the internet with this visualization tool.</div>
            <div className="home-signup"><a href="/signup"><button className="btn-signup">Create your dashboard</button></a></div>
        </div>
    )
}

export default Home