import { useCityStore } from '../../../../stores/City';
import { ref, watch, onMounted } from 'vue'
export const backMapHook = ($router) => {
    const $store = useCityStore();
    const { changeCity, changeHistoryCities } = useCityStore();
    const back = (city) => {
        $router.back()
        console.log(city)
        changeCity(city);
        changeHistoryCities(city);
        /* 历史记录 */


    }
    return { back };
}
