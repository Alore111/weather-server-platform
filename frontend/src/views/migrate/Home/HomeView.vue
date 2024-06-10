<template>
  <NavBar @handle-search="handleSearch"></NavBar>
  <div id="map"></div>
  <Weather :result="data" />
</template>
<script setup>
import { getCurrentInstance } from "vue";
import Weather from "./components/Weather.vue";
import NavBar from "./components/NavBar.vue";
import { getCityCodeHttp } from "../../../api";
/* 1、初始化地图 */
import { initMap } from "./Hooks/initMap";
/* 2、实现地图的飞行 */
import { FlyTo } from "./Hooks/flyTo";
/* 3、从城市页面跳转回首页 */
import { backMap } from "./Hooks/InitMapEvent";
import { onMounted } from "vue";
import { useCityStore } from "../../../stores/City";
const $store = useCityStore();
initMap();
// FlyTo();
let data = backMap();
let map = null;
onMounted(() => {
  const { proxy } = getCurrentInstance();
  map = proxy.$map;
});
const handleSearch = async (val) => {
  const result = await getCityCodeHttp(val.value);
  let { adcode, location } = result.data.geocodes[0];
  let center = location.split(",");
  var res = await FlyTo(center, adcode, map);
  data.value = res;
};
</script>
