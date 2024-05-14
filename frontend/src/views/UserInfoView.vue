<template>
    <el-descriptions title="基本信息">
        <el-descriptions-item label="用户名">{{ username }}</el-descriptions-item>
        <el-descriptions-item label="用户ID">{{ id }}</el-descriptions-item>
        <el-descriptions-item label="绑定QQ">{{ qq }}</el-descriptions-item>
    </el-descriptions>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            id: '',
            qq: ''
        }
    },
    mounted() {
        this.refershUserInfo();
    },
    methods: {
        refershUserInfo() {
            const user_info_str = localStorage.getItem('user_info');
            // console.log(user_info_str);
            if (user_info_str) {
                const user_info = JSON.parse(user_info_str);
                this.id = "" + user_info['id'];
                this.qq = "" + user_info['qq'];
                this.username = user_info['username'];
            }
        },
    }
};
</script>

<style>
.el-descriptions__body {
    background-color: #ececec;
}
</style>