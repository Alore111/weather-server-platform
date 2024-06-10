<template>
  
  <van-button
    @click="back(item.name) && back"
    v-for="item of hotCities"
    :key="item.id"
    >{{ item.name }}
  </van-button>
</template>

<script setup>
import { backMapHook } from "./backMapHook";
import { useRouter } from "vue-router";
const { back } = backMapHook(useRouter());
defineProps({
  hotCities: {
    type: Object,
  },
});
</script>

<style scoped>
.van-button {
  margin-right: 20px;
  border-radius: 5px;
  margin-top: 5px;
}

h4 {
  color: #666;
  line-height: 40px;
}
</style>
