<template>
    <div id="page-container" class="main-content-boxed">
        <main id="main-container">
            <div class="bg-image"
                :style="{ 'background-image': 'url(https://cdnjson.com/images/2024/05/14/clouds-1282314_19204a2556ad63d1149c.jpg)' }">
                <div class="row mx-0 bg-earth-op">
                    <div class="hero-static col-md-6 col-xl-8 d-none d-md-flex align-items-md-end">
                        <div class="p-4">
                            <p class="fs-3 fw-semibold text-white mb-1">
                                We're very happy you are joining our community!
                            </p>
                            <p class="fs-5 text-white fw-medium">
                                <i class="fa fa-angle-right opacity-50"></i> Create your account today !
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
                                <h1 class="h3 fw-bold mt-4 mb-2">创建新账户</h1>
                                <h2 class="h5 fw-medium text-muted mb-0">请填写您的详细资料</h2>
                            </div>
                            <form class="js-validation-signup px-4" @submit.prevent="ajaxUserReg">
                                <div class="form-floating mb-4">
                                    <input v-model="username" class="form-control" id="username" name="username"
                                        placeholder="输入你的用户名" type="text">
                                    <label class="form-label" for="username">用户名</label>
                                </div>
                                <div class="form-floating mb-4">
                                    <input v-model="password" class="form-control" id="password" name="password"
                                        placeholder="输入你的密码" type="password">
                                    <label class="form-label" for="password">密码</label>
                                </div>
                                <div class="form-floating mb-4">
                                    <input v-model="qq" class="form-control" id="qq" name="qq" placeholder="输入你的QQ"
                                        type="number">
                                    <label class="form-label" for="qq">QQ(通知/登录/找回密码时使用)</label>
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
                                            <div><img id="captchaImg" class="border"
                                                    :src="this.$serverUrl + '/api/captcha'" @click="refreshCaptcha()"
                                                    alt="captcha" height="58px;" width="100%" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <!-- <div class="mb-4">
                                    <div class="form-check">
                                        <input v-model="agreeTerms" class="form-check-input" id="signup-terms"
                                            name="signup-terms" type="checkbox">
                                        <label class="form-check-label" for="signup-terms">我同意条款</label>
                                    </div>
                                </div> -->
                                <div class="mb-4">
                                    <button @click="userRegister" class="btn btn-lg btn-alt-primary fw-semibold"
                                        type="submit">创建账户</button>
                                    <div class="mt-4">
                                        <router-link class="fs-sm fw-medium link-fx text-muted me-2 mb-1 d-inline-block"
                                            to="/login">返回登录</router-link>

                                        <router-link class="fs-sm fw-medium link-fx text-muted me-2 mb-1 d-inline-block"
                                            to="/find">找回密码</router-link>

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
            qq: '',
            captcha: '',
            captcha_seed: '',
            // agreeTerms: false,
        };
    },
    computed: {
        currentYear() {
            return new Date().getFullYear();
        },
    },
    mounted() {
        // 初始化验证码
        this.refreshCaptcha();
    },
    methods: {
        userRegister() {

            if (!this.username || !this.password || !this.qq || !this.captcha) {
                ElMessage({
                    message: '请填写完整信息',
                    type: 'warning',
                })
                return;
            }

            const loading = ElLoading.service({
                lock: true,
                text: '正在注册',
                background: 'rgba(0, 0, 0, 0.7)',
            })


            const formData = new FormData();
            formData.append('username', this.username);
            formData.append('password', this.password);
            formData.append('qq', this.qq);
            formData.append('captcha', this.captcha);
            formData.append('captcha_seed', this.captcha_seed);

            fetch(this.$serverUrl + '/api/register', {
                method: 'POST',
                body: formData
            })
                .then(res => res.json())
                .then(res => {
                    loading.close();
                    if (res["code"] == 200) {
                        ElMessage({
                            message: '注册成功',
                            type: 'success',
                        })
                        this.$router.push('/login');
                    } else {
                        ElMessage({
                            message: res["message"],
                            type: 'error',
                        })
                    }

                })
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