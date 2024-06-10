<template>
    <van-index-bar :index-list="Object.keys(cities)">
        <van-index-anchor :index="index" v-for="item, index of cities" :key="index">
            {{ index }}
            <van-cell @click="back(val.name)" v-for="val of item"  :key="val.name" :title="val.name" />
        </van-index-anchor>


    </van-index-bar>
</template>
    
<script setup>
import { backMapHook } from './backMapHook'
import { useRouter } from 'vue-router'
const { back } = backMapHook(useRouter());
const props = defineProps({
    cities: {
        type: Object
    }
})
</script>
    
<style>
.van-cell:hover {
    background-color: #eee !important;
    cursor: pointer;
}
</style>