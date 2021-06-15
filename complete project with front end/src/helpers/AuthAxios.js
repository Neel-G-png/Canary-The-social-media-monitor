import axios from "axios";

const token = "JWT " + localStorage.getItem("token");

export const AuthAxios = axios.create({
    baseURL: "http://127.0.0.1:5000",
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "Authorization": token ? token : null
    },
});