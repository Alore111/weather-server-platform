<template>
  <el-menu
    class="el-menu-demo"
    mode="horizontal"
    background-color="#4264fb"
    text-color="#fff"
    active-text-color="#ffd04b"
  >
    <el-menu-item index="1" @click="jumpCity">
      {{ city }}
      <i class="qi-301"></i>
      <i class="iconfont icon-ditu_dingwei"></i>
    </el-menu-item>
    <el-menu-item>
      <el-input
        class="input"
        @keydown.enter="handleEnter"
        v-model="search"
        placeholder="请搜索你所在的城市"
        :prefix-icon="Search"
      />
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { Search } from "@element-plus/icons-vue";
import { useRouter } from "vue-router";
import { ref } from "vue";
import { useCityStore } from "../../../../stores/City";
import { storeToRefs } from "pinia";
/* 获取当前城市数据 */
const { city } = storeToRefs(useCityStore());
/* 跳转到城市页面 */
const $router = useRouter();
const jumpCity = () => {
  $router.push("/city");
};
const search = ref("");
const $emit = defineEmits(["handleSearch"]);
const handleEnter = () => {
  $emit("handleSearch", search);
};
</script>
<style>
.el-menu-demo {
  align-items: center;
}

.el-menu-demo .is-active {
  border-bottom-color: transparent !important;
}

.input {
  width: 300px !important;
  height: 40px;
}

.el-menu-demo .el-menu-item:nth-child(2):hover {
  background-color: transparent !important;
}

.icon-ditu_dingwei {
  color: #ff2d51 !important;
  font-size: 20px !important;
}
</style>
