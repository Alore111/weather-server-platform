<template>
    <div id="page-container" class="main-content-boxed">
        <main id="main-container">
            <div class="bg-image"
                :style="{ 'background-image': 'url(https://cdnjson.com/images/2024/05/14/clouds-1282314_19204a2556ad63d1149c.jpg)' }">
                <div class="row mx-0 bg-default-op">
                    <div class="hero-static col-md-6 col-xl-8 d-none d-md-flex align-items-md-end">
                        <div class="p-4">
                            <p class="fs-3 fw-semibold text-white">
                                You are awesome! Build something amazing!
                            </p>
                            <p class="text-white-75 fw-medium">
                                Copyright &copy; <span data-toggle="year-copy">{{ currentYear }}</span>
                            </p>
                        </div>
                    </div>
                    <div class="hero-static col-md-6 col-xl-4 d-flex align-items-center bg-body-extra-light">
                        <div class="content content-full">
                            <div class="px-4 py-2 mb-4">
                                <router-link class="link-fx fw-bold" to="#">
                                    <i class="fas fa-key"></i>
                                    <span class="fs-4 text-body-color">Weather Vista</span>
                                </router-link>
                                <h1 class="h3 fw-bold mt-4 mb-2">重置密码</h1>
                                <h2 class="h5 fw-medium text-muted mb-0" v-if="!tokenOK">链接无效</h2>
                                <h2 class="h5 fw-medium text-muted mb-0" v-else>请输入您的新密码</h2>
                            </div>
                            <template v-if="!tokenOK">
                                <div class="alert alert-warning" role="alert">
                                    <p>您的链接无效，请确保链接正确。</p>
                                    <p>错误信息：{{ tokenOKMsg }}</p>
                                </div>
                            </template>
                            <template v-else>
                                <form class="js-validation-reset px-4" @submit.prevent="userResetPassword">
                                    <div class="form-floating mb-4">
                                        <input v-model="form.password" class="form-control" id="password"
                                            name="password" placeholder="请输入新密码" type="password"
                                            autocomplete="new-password">
                                        <label class="form-label" for="password">新密码</label>
                                    </div>
                                    <div class="form-floating mb-4">
                                        <input v-model="form.confirmPassword" class="form-control" id="confirmPassword"
                                            name="confirmPassword" placeholder="请确认新密码" type="password"
                                            autocomplete="new-password">
                                        <label class="form-label" for="confirmPassword">确认密码</label>
                                    </div>
                                    <div class="mb-4">
                                        <button type="submit" class="btn btn-lg btn-alt-primary fw-semibold" v-loading="isSubmitting"
                                            :disabled="isSubmitting">
                                            提交
                                        </button>
                                    </div>
                                    <el-alert v-if="error" type="error" :closable="false">{{ error }}</el-alert>
                                </form>
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
</template>

<script>
import axios from 'axios';
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { ElLoading } from 'element-plus';

export default {
    data() {
        return {
            viewLoading: true,
            tokenOK: true,
            tokenOKMsg: '',
            token: null,
            form: reactive({
                password: '',
                confirmPassword: '',
            }),
            error: null,
            isSubmitting: false,
        };
    },
    mounted() {
        const params = new URLSearchParams(window.location.search);
        this.token = params.get('token');
        if (this.token == null) {
            this.error = '链接无效';
            this.tokenOK = false;
            this.tokenOKMsg = '链接无效';
            this.viewLoading = false;
        } else {
            fetch(this.$serverUrl + '/api/checkResetToken?reset_token=' + this.token, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then(response => response.json())
                .then(data => {
                    this.viewLoading = false;
                    if (data.code !== 200) {
                        this.error = '链接无效';
                        this.tokenOK = false;
                        this.tokenOKMsg = data['message'];
                    }
                })
                .catch(error => {
                    console.error('错误：', error);
                });
        }
    },
    methods: {
        userResetPassword() {
            // 清除之前的错误信息
            this.error = null;

            // 检查新密码和确认密码是否匹配
            if (this.form.password !== this.form.confirmPassword) {
                this.error = '密码和确认密码不匹配';
                return;
            }

            // 检查新密码长度
            if (this.form.password.length < 6) {
                this.error = '新密码长度不能少于6个字符';
                return;
            }

            // 提交表单数据
            this.isSubmitting = true;
            let dataForm = new FormData();
            dataForm.append('reset_token', this.token);
            dataForm.append('password', this.form.password);
            axios.post(this.$serverUrl + '/api/resetPassword', dataForm)
                .then(response => {
                    if (response.data.code === 200) {
                        ElMessage({
                            message: '密码重置成功',
                            type: 'success',
                        });
                        this.$router.push('/login');
                    } else {
                        this.error = response.data.message;
                    }
                })
                .catch(error => {
                    console.error('错误：', error);
                })
                .finally(() => {
                    this.isSubmitting = false;
                });
        },
    },
    computed: {
        currentYear() {
            return new Date().getFullYear();
        },
    },

};
</script>


<style scoped>
/* 您的组件特定样式在这里 */
</style>
