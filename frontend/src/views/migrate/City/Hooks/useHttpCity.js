import axios from "axios";
import { onMounted, ref } from "vue";
import { getCityHttp } from "../../../../api";
export const useCity = () => {
    const hotCities = ref([]);
    const cities = ref([]);
    onMounted(async () => {
        let result = await getCityHttp();
        let data = result.data.data;
        hotCities.value = data.hotCities
        cities.value = data.cities;
    })
    return {
        hotCities,
        cities
    }
}