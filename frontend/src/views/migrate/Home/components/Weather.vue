
<template>
    <div class="weather">
        <table>
            <tr v-for="item of result" :key="item">
                <td>{{item.name}} </td>
                <td>{{item.val}}</td>
            </tr>
        </table>
    </div>
</template>
<script setup>
defineProps({
    result:{
        type:Object
    }
})
</script>
<style scoped>
.weather{
    position: fixed;
    right:20px;
    top:70px;
    z-index: 100;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 0 3px 2px #333;
    background: #2193b0a1;  /* fallback for old browsers */
background: -webkit-linear-gradient(to top, #6dd5ed, #2193b0);  /* Chrome 10-25, Safari 5.1-6 */
background: linear-gradient(to top, #6dd5edb0, #2193b0); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
table,td{
    border-collapse: collapse;
    
}
td{
border:1px solid rgba(238, 238, 238, 0.473);
}
table{
    color:#fff;
    text-align: center;
    width:200px;
    line-height: 30px;
    border-radius: 15px;
}
</style>