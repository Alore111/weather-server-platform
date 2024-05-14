<template>
    <div id="page-container" class="main-content-boxed">
        <main id="main-container">
            <div class="bg-image" :style="{ 'background-image': 'url(https://cdnjson.com/images/2024/05/14/clouds-1282314_19204a2556ad63d1149c.jpg)' }">
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
                                    <i class="fas fa-cloud"></i>
                                    <span class="fs-4 text-body-color">Weather Vista</span>
                                </router-link>
                                <h1 class="h3 fw-bold mt-4 mb-2">找回账户密码</h1>
                                <h2 class="h5 fw-medium text-muted mb-0">请输入你的邮箱</h2>
                            </div>
                            <form class="js-validation-reminder px-4" @submit.prevent="userFind">
                                <div class="form-floating mb-4">
                                    <input v-model="mail" class="form-control" id="mail" name="mail"
                                        placeholder="输入你的邮箱" type="text">
                                    <label class="form-label">邮箱(以“@qq.com”结尾)</label>
                                    <div class="text-muted fs-xs">邮箱默认为您的QQ账号邮箱</div>
                                </div>
                                <div class="row mb-4">
                                    <div class="col-6">
                                        <div class="form-floating">
                                            <input v-model="captcha" class="form-control" id="captcha" name="captcha"
                                                placeholder="请输入验证码" type="text">
                                            <label class="form-label" for="captcha">验证码</label>
                                        </div>
                                    </div>
                                    <div class="col-6">
                                        <div class="form-floating">
                                            <div><img id="captchaImg" class="border" :src="this.$serverUrl + '/api/captcha'"
                                                    @click="refreshCaptcha()" alt="captcha" height="58px;" width="100%" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="mb-4">
                                    <button type="submit" class="btn btn-lg btn-alt-primary fw-semibold" v-loading="this.btnLoding" :disabled="mail.length === 0 || captcha.length === 0 || this.btnLoding">找回密码</button>
                                    <div class="mt-4">
                                        <router-link class="fs-sm fw-medium link-fx text-muted me-2 mb-1 d-inline-block"
                                            to="/login">
                                            <i class="fa fa-arrow-left opacity-50 me-1"></i> 返回登录
                                        </router-link>
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
import { ElMessage } from 'element-plus';

export default {
    data() {
        return {
            mail: '',
            captcha: '',
            captcha_seed: '',
            btnLoding: false,
        };
    },
    computed: {
        currentYear() {
            return new Date().getFullYear();
        },
    },
    mounted() {
        this.refreshCaptcha();
    },
    methods: {
        userFind() {
            this.btnLoding = true;

            if(!this.mail.includes("@qq.com")){
                ElMessage({
                    message: '请输入正确的邮箱',
                    type: 'warning',
                });
                this.btnLoding = false;
                return false;
            }


            const formData = new FormData();
            formData.append('email', this.mail);
            formData.append('captcha', this.captcha);
            formData.append('captcha_seed', this.captcha_seed);
            console.log(formData);
        

            fetch(this.$serverUrl + '/api/find', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    this.btnLoding = false;
                    if (data.code === 200) {
                        ElMessage({
                            message: '重置邮件发送成功，请查收',
                            type: 'success',
                        });
                        this.$router.push('/login');
                    } else {
                        ElMessage({
                            message: data.message,
                            type: 'warning',
                        });
                    }
                })
                .catch(error => {
                    this.btnLoding = false;
                    console.error('Error:', error);
                    ElMessage({
                            message: '邮件发送失败，请稍后再试',
                            type: 'warning',
                        });
                });
            this.refreshCaptcha();
            this.captcha = '';
            return false;
        },
        refreshCaptcha() {
            console.log('refresh captcha');
            this.captcha_seed = Math.floor(Math.random() * 1000000000);
            document.getElementById('captchaImg').src = this.$serverUrl + '/api/captcha?seed=' + this.captcha_seed;
        },
    },
};
</script>

<style scoped>
/* Your component-specific styles here */
</style>