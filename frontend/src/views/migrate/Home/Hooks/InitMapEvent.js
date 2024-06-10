import { onActivated, ref, getCurrentInstance } from "vue";
import { getCityCodeHttp, getWeatherHttp } from '../../../../api'
import { FlyTo } from "./flyTo";
import { useCityStore } from "../../../../stores/City";
export const backMap = () => {
    const weatherData = ref(null)
    onActivated(async () => {
        const { proxy } = getCurrentInstance();
        let $map = proxy.$map
        let store = useCityStore()
        /* 判断缓存中是否有城市 */
        if (store.city) {
            const result = await getCityCodeHttp(store.city);
            let { adcode, location } = result.data.geocodes[0]
            let center = location.split(",")
            let res = await FlyTo(center, adcode, $map);
            /* 获取天气数据 */
            weatherData.value = res;
        }
    })
    return weatherData;
}