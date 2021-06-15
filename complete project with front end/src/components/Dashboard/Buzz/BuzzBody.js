import React from 'react';
import youtube from "../../../assets/youtube.png"
import reddit from "../../../assets/reddit.png"
import google from "../../../assets/google.png"
import twitter from "../../../assets/twitter.png"
import upvote from "../../../assets/upvote.png"
import fire from "../../../assets/fire2.png"

import "./Buzz.css"

export default function BuzzBody({ data }) {
    const imgHandler = value => {
        switch (value) {
            case 'Reddit':
                return reddit;
            case 'Youtube':
                return youtube;
            case 'Twitter':
                return twitter;
        }
    };
    return (
        <a className="panel-block All" href={data.link}>
            <div className="buzzcard">
                <div className="flex-column">
                    <div className="d-flex ml-2 font-weight-bold">
                        <div ><img src={imgHandler(data.site)} style={{ height: 20, width: 20, borderRadius: "60%" }} /></div>
                        <span className="ml-2">{data.site}</span>
                    </div>
                    <div className="ml-2" style={{ width: 520 }}>{data.title}</div>
                </div>
                <div className="flex-column">
                    <div className="mr-2"><img src={upvote} style={{ height: 20, width: 20, borderRadius: "60%" }} /></div>
                    <div>{data.outreach}</div>
                </div>
            </div>
        </a>
    );
}
