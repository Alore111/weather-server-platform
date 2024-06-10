import { ref, watch } from 'vue'
import { defineStore } from 'pinia'

export const useCityStore = defineStore('city', () => {
    const getDefaultCity = () => {
        let city = ref("武汉")
        if (localStorage.getItem("city")) {
            city.value = localStorage.getItem("city")
        }
        return city;
    }
    const city = getDefaultCity();

    const changeCity = (val) => {
        city.value = val;
        localStorage.setItem("city", val)
    }
    const getHistoryCities = () => {
        let cities = ref([]);
        let localCities = JSON.parse(localStorage.getItem("historyCity"));
        if (localCities) {
            cities.value = localCities;
        }
        return cities;
    }
    const historyCities = getHistoryCities();
    const changeHistoryCities = (city) => {
        if (!historyCities.value.includes(city)) {
            historyCities.value.unshift(city)
            /* 限制数据长度 */
            historyCities.value = historyCities.value.slice(0, 3)
        } else {
            let index = historyCities.value.indexOf(city);
            historyCities.value.splice(index, 1);
            historyCities.value.unshift(city)
        }
    }
    watch(historyCities, val => {
        /* 设置缓存 */
        console.log(val)
        localStorage.setItem("historyCity", JSON.stringify(val));
    })
    return { city, changeCity, historyCities, changeHistoryCities }
})