<template>
  <div class="city-container">
    <h4>当前城市</h4>
    <van-button class="current">{{ city }}</van-button>
    <h4>定位/最近访问</h4>
    <van-button> <i class="iconfont icon-ditu_dingwei"></i> 武汉</van-button>
    <van-button v-for="item of historyCities" :key="item">{{
      item
    }}</van-button>
    <h4>热门城市</h4>
    <HotCity :hot-cities="hotCities" />
    <ListCity :cities="cities" />
  </div>
</template>
<script setup>
import { useCity } from "./Hooks/useHttpCity";
import HotCity from "./components/HotCity.vue";
import ListCity from "./components/ListCity.vue";
import { useCityStore } from "../../../stores/City";
import { storeToRefs } from "pinia";
const { hotCities, cities } = useCity();
const { city, historyCities } = storeToRefs(useCityStore());
console.log(historyCities);
</script>
<style scoped>
.city-container h4 {
  text-indent: 15px;
  line-height: 40px;
  color: #666;
  font-size: 16px;
  font-weight: lighter;
  background-color: #efeeee;
  margin: 6px 0px;
}
.van-button {
  margin-left: 5px;
}
.icon-ditu_dingwei {
  color: #4164fb !important;
}
.current {
  background-color: #198754 !important;
  color: #fff;
}
</style>
