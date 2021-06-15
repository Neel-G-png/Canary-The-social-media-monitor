import axios from "axios";

const token = "JWT " + localStorage.getItem("token");
const user = localStorage.getItem("user");

const AxiosInstance = axios.create({
    // baseURL: "https://6be432d6-577c-4430-9cf4-baf9ef1fcaeb.mock.pstmn.io",
    // baseURL: "https://9d1b1a84-5fe5-473f-80ce-b25b49ed92bd.mock.pstmn.io",
    baseURL: "http://127.0.0.1:5000",
    // baseURL: "https://831360ab-ab44-4c62-a008-bd264c531793.mock.pstmn.io",
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "Authorization": token,
        "userID": user
    },
});

export default AxiosInstance


