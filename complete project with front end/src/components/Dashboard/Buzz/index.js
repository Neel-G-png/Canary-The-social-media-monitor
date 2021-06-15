import React, { useState, useContext, useEffect } from 'react'
import "../Dashboard.css"
// import { Data } from './Data';
import BuzzBody from './BuzzBody';
import browser from "../../../assets/browser.png"
import youtube from "../../../assets/youtube.png"
import reddit from "../../../assets/reddit.png"
import google from "../../../assets/google.png"
import twitter from "../../../assets/twitter.png"
import Tooltip from 'react-bootstrap/Tooltip'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger'
import { buzz } from "../../../context/actions/dashboard"
import { GlobalContext } from "../../../context/Provider"


export default function Index() {
  const [active, setActive] = useState('All');

  const handleActiveClick = value => {
    setActive(value);
  };

  const { dashboardState } = useContext(GlobalContext);

  console.log("buzz data->", dashboardState.buzzData)

  const Data = dashboardState.buzzData.items

  return (
    <div className="buzz">
      <OverlayTrigger
        placement={'right'}
        overlay={
          <Tooltip style={{ opacity: 0.7 }} >
            See all the mentions of your brand across various social media platforms
        </Tooltip>
        }
      >
        <div className="card-title text-left">Social Media Buzz </div>
      </OverlayTrigger>

      <article className="panel is-info">
        <p className="panel-tabs is-boxed">
          <a
            name="All"
            className={active === 'All' ? 'd-flex d-flex is-active' : 'd-flex'}
            onClick={e => handleActiveClick('All')}>
            <div className="mr-2"><img src={browser} style={{ height: 20, width: 20 }} /></div>

                        All
          </a>
          <a
            name="Reddit"
            className={active === 'Reddit' ? 'd-flex is-active' : 'd-flex'}
            onClick={e => handleActiveClick('Reddit')}>
            <div className="mr-2"><img src={reddit} style={{ height: 20, width: 20 }} /></div>

                        Reddit
          </a>
          <a
            name="Youtube"
            className={active === 'Youtube' ? 'd-flex is-active' : 'd-flex'}
            onClick={e => handleActiveClick('Youtube')}>
            <div className="mr-2"><img src={youtube} style={{ height: 20, width: 20 }} /></div>

                        Youtube
          </a>
          <a
            name="Twitter"
            className={active === 'Twitter' ? 'd-flex is-active' : 'd-flex'}
            onClick={e => handleActiveClick('Twitter')}>
            <div className="mr-2"><img src={twitter} style={{ height: 20, width: 20 }} /></div>

                        Twitter
          </a>
        </p>

        {active === 'All'
          ? Data.map(i => <BuzzBody data={i} />)
          : active === 'Reddit'
            ? Data.filter(i => i.site === 'Reddit').map(i => <BuzzBody data={i} />)
            : active === 'Youtube'
              ? Data.filter(i => i.site === 'Youtube').map(i => <BuzzBody data={i} />)
              : active === 'Twitter'
                ? Data.filter(i => i.site === 'Twitter').map(i => <BuzzBody data={i} />)
                : null}
      </article>
    </div>
  );
}

