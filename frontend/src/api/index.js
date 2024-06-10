import axios from "axios"
/* 获取城市也页的数据 */
var key = '0d0f38ca993c65d51f508675413e4a4c'
const getCityHttp = () => {
    return axios.get("http://39.103.151.139:8000/city")
}
const getCityCodeHttp = (city) => {
    return axios.get(`https://restapi.amap.com/v3/geocode/geo?address=${city}&key=${key}`)
}
const getWeatherHttp = (code) => {
    return axios.get(`https://restapi.amap.com/v3/weather/weatherInfo?city=${code}&key=${key}`)
}
export { getCityHttp, getCityCodeHttp, getWeatherHttp };