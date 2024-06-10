import { ref } from 'vue'
import { defineStore } from 'pinia'
export const useMapStore = defineStore('map', () => {
    const map = ref("")
    const geojsonLayer = new ol.layer.Vector({})
    const changemap = (val) => {
        map.value = val;
    }
    return { map, changemap,geojsonLayer}
})