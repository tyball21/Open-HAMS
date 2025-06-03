import axios from "axios";
import { API_URL } from "./utils";

const instance = axios.create({
  baseURL: API_URL,
  timeout: 40000,
  timeoutErrorMessage: "Request timed out",
  validateStatus(code) {
    return true;
  },
});

instance.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  
  // Only set Content-Type to application/json if we're not sending FormData
  // Let axios automatically set the Content-Type for FormData requests
  if (!(config.data instanceof FormData)) {
    config.headers["Content-Type"] = "application/json";
  }
  
  return config;
});

instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      console.log("Unauthorized");
      localStorage.removeItem("token");
      window.location.href = "/";
    }
    return Promise.reject;
  },
);

export default instance;
