<template>
    <div id="page-container" class="main-content-boxed">
        <main id="main-container">
            <div class="bg-image"
                :style="{ 'background-image': 'url(https://cdnjson.com/images/2024/05/14/clouds-1282314_19204a2556ad63d1149c.jpg)' }">
                <div class="row mx-0 bg-black-50">
                    <div class="hero-static col-md-6 col-xl-8 d-none d-md-flex align-items-md-end">
                        <div class="p-4">
                            <p class="fs-3 fw-semibold text-white">
                                Get Inspired and Create.
                            </p>
                            <p class="text-white-75 fw-medium">
                                Copyright &copy; <span v-text="currentYear"></span>
                            </p>
                        </div>
                    </div>
                    <div class="hero-static col-md-6 col-xl-4 d-flex align-items-center bg-body-extra-light">
                        <div class="content content-full">
                            <div class="px-4 py-2 mb-4">
                                <router-link class="link-fx fw-bold" to="#">
                                    <i class="fas fa-cloud"></i>
                                    <span class="fs-4 text-body-color">Weather Vista</span>
                                </router-link>
                                <h1 class="h3 fw-bold mt-4 mb-2">欢迎来到您的用户中心</h1>
                                <h2 class="h5 fw-medium text-muted mb-0">请登录</h2>
                            </div>
                            <form class="js-validation-signin px-4" @submit.prevent="ajaxUserLogin">
                                <div class="form-floating mb-4">
                                    <input v-model="username" class="form-control" id="username" name="username"
                                        placeholder="输入你的用户名/qq/邮箱" type="text">
                                    <label class="form-label" for="username">用户名/qq/邮箱</label>
                                </div>
                                <div class="form-floating mb-4">
                                    <input v-model="password" class="form-control" id="password" name="password"
                                        placeholder="输入你的密码" type="password">
                                    <label class="form-label" for="password">密码</label>
                                </div>
                                <div class="mb-4">
                                    <div class="form-check">
                                        <input v-model="rememberMe" class="form-check-input" id="login-remember-me"
                                            name="login-remember-me" type="checkbox" value="true">
                                        <label class="form-check-label" for="login-remember-me">记住我</label>
                                    </div>
                                </div>
                                <div class="mb-4">
                                    <button class="btn btn-lg btn-alt-primary fw-semibold" type="submit"
                                        @click="userLogin">登录</button>
                                    <div class="mt-4">
                                        <router-link class="fs-sm fw-medium link-fx text-muted me-2 mb-1 d-inline-block"
                                            to="/register">创建账户</router-link>

                                        <router-link class="fs-sm fw-medium link-fx text-muted me-2 mb-1 d-inline-block"
                                            to="/find">忘记密码?</router-link>


                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import { ElLoading } from 'element-plus'
import { ElMessage } from 'element-plus'
export default {
    data() {
        return {
            username: '',
            password: '',
            rememberMe: false,
        };
    },
    computed: {
        currentYear() {
            return new Date().getFullYear();
        },
    },
    methods: {
        userLogin() {
            // 验证用户名和密码是否为空
            if (!this.username || !this.password) {
                ElMessage({
                    message: '用户名和密码不能为空',
                    type: 'error',
                });
                return; // 如果用户名或密码为空，则停止执行登录逻辑
            }

            const formData = new FormData();
            formData.append('username', this.username);
            formData.append('password', this.password);
            formData.append('rememberMe', this.rememberMe);

            const loading = ElLoading.service({
                lock: true,
                text: '登录中',
                background: 'rgba(0, 0, 0, 0.7)',
            })

            fetch(this.$serverUrl + '/api/login', {
                method: 'POST',
                body: formData,
            })
                .then(response => {
                    loading.close();
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // console.log('Success:', data);
                    if (data.login === true) {
                        // 登录成功，保存用户信息和访问令牌到 localStorage
                        localStorage.setItem('user_info', JSON.stringify(data.user_info));
                        localStorage.setItem('access_token', data.access_token);

                        // 处理成功登录的逻辑
                        ElMessage({
                            message: '登录成功',
                            type: 'success',
                        });
                        setTimeout(() => {
                            this.$router.push('/console');
                        }, 1000);
                    } else {
                        // 处理登录失败的逻辑
                        ElMessage({
                            message: '登录失败，请检查用户名和密码',
                            type: 'warning',
                        });
                    }
                })
                .catch(error => {
                    loading.close();
                    console.error('Error:', error);
                    // 处理异常情况
                    ElMessage({
                        message: '网络请求失败，请稍后重试',
                        type: 'error',
                    });
                });
        }



    },
};
</script>



<style scoped>
/* Your component-specific styles here */
</style>