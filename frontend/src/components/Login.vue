<template>
    <div>
        <el-input placeholder="请输入账户名" v-model="usename">
            <template slot="prepend">账号：</template>
        </el-input>
        <el-input placeholder="请输入密码" v-model="password">
            <template slot="prepend">密码：</template>
        </el-input>
        <el-button type="primary" @click="toHome">登录</el-button>
    </div>
</template>

<script>
export default {
    name: 'Login',
    data() {
        return {
            usename: '',
            password: '',
        }
    },
    methods: {
        //点击登录按钮执行访问请求并判断是否登陆
        toHome() {

        }
    }
}
</script>