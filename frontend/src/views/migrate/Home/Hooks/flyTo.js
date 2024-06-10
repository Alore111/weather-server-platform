import { useMapStore } from "../../../../stores/Map"
import { getWeatherHttp } from "../../../../api";
import { getCurrentInstance, onMounted } from 'vue'
export const FlyTo = async (center = [114, 30], adcode, $map) => {
    const { map, geojsonLayer } = useMapStore();
    const view = $map.getView();
    setTimeout(() => {
        /* 1、飞行 */
        view.animate({
            center,
            zoom: 8,
            duration: 3000
        })
        /* 2、加载地形数据 */
        var url = `https://geo.datav.aliyun.com/areas_v3/bound/${adcode}.json`;
        var source = new ol.source.Vector({
            url,
            format: new ol.format.GeoJSON()//解析geojson数据
        })
        let style = new ol.style.Style({
            // 形状
            fill: new ol.style.Fill({
                color: 'rgba(0,0,0,0.5)'
            }),
            /* 描边 */
            stroke: new ol.style.Stroke({
                color: '#ff2d51',
                width: 2
            })
        })
        // var layer = new ol.layer.Vector({
        //     source,
        //     style
        // })
        geojsonLayer.setSource(null);
        geojsonLayer.setSource(source);
        geojsonLayer.setStyle(style)
        map.addLayer(geojsonLayer)
    }, 2000)
    /* 3、获取天气数据 */
    const weatherRes = await getWeatherHttp(adcode);
    var { city, weather, temperature, winddirection, windpower } = weatherRes.data.lives[0];
    return {
        city: { val: city, name: "城市" },
        weather: { val: weather, name: "天气" },
        temperature: { val: temperature, name: "温度" },
        winddirection: { val: winddirection, name: "风向" },
        windpower: { val: windpower, name: "风力" }
    }

}