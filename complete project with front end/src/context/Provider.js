import React, { createContext, useReducer, useState, useEffect } from "react";
import auth from "./reducers/auth";
import dashboard from "./reducers/dashboard";
import { authInitial, dashboardInitial } from "./InitialState"
import io from "socket.io-client";

let endPoint = "http://localhost:5000";
let socket = io.connect(`${endPoint}`);

export const GlobalContext = createContext({});

export const GlobalProvider = ({ children }) => {
    const [authState, authDispatch] = useReducer(auth, authInitial);
    const [dashboardState, dashboardDispatch] = useReducer(dashboard, dashboardInitial);

    const [time, setTime] = useState(1)

    const getTime = () => {
        socket.emit("getTime")
        socket.on("getTime", timenew => {
            setTime(timenew);
            // console.log("get time was called ->", timenew)
        });
    };

    // useEffect(() => {
    //     getTime();
    // }, []);


    return (
        <GlobalContext.Provider
            value={{
                authState,
                authDispatch,
                time: time,
                dashboardState,
                dashboardDispatch
            }}
        >
            {children}
        </GlobalContext.Provider>
    );
};