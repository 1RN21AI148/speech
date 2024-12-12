import axios from "axios";
import { BASE_URL } from "../utils/constants";


const instance = axios.create({
    baseURL: BASE_URL,
    timeout: 3000,
})


export default instance
