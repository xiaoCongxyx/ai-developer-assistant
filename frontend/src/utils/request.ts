import axios from "axios";

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 10000
})

request.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error', error)
    return Promise.reject(error)
  }
)


export default request