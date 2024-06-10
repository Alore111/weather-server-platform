import { onMounted } from 'vue';
import { useMapStore } from '../../../../stores/Map';
import { app } from '../../../../main.js'
export const initMap = () => {
    const { changemap } = useMapStore();
    onMounted(() => {
        var gaodeMapLayer = new ol.layer.Tile({
            title: "高德地图",
            source: new ol.source.XYZ({
                url: 'http://wprd0{1-4}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&style=7&x={x}&y={y}&z={z}',
                wrapX: false
            })
        });
        const map = new ol.Map({
            target: "map",
            layers: [gaodeMapLayer],
            view: new ol.View({
                projection: 'EPSG:4326',
                center: [114, 30],
                zoom: 5
            })
        })
        app.config.globalProperties.$map = map
        changemap(map);
    })
}
