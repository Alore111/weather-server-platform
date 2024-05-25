<template>
    <div class="common-layout">
        <el-container>
            <el-header>
                <div style="position: relative; left: 10px" class="collapse-btn" @click="toggleCollapse">
                    <i class="fas"
                        :class="{ 'fa-chevron-left': !asideCollapsed, 'fa-chevron-right': asideCollapsed }">{{
                            asideCollapsed ? '菜单' : '收起' }}</i>
                </div>
                <router-link class="link-fx fw-bold" to="#">
                    <i class="fas fa-cloud"></i>
                    <span class="fs-4 text-body-color">Weather Vista</span>
                </router-link>
                <div>
                    <el-button type="primary" @click="userLogout" plain>退出登录</el-button>
                </div>
            </el-header>
            <el-container>
                <el-aside width="200px"
                    :style="{ transform: asideCollapsed ? 'translateX(-100%)' : 'none', position: asideCollapsed ? 'fixed' : '' }">
                    <el-menu default-active="" class="el-menu-vertical-demo">
                        <router-link to="/console/">
                            <el-menu-item index="0">
                                <i class="fas fa-home m-1"></i>
                                <span style="font-weight: 600;">HOME</span>
                            </el-menu-item>
                        </router-link>
                        <el-sub-menu index="1">
                            <template #title>
                                <el-icon>
                                    <i class="far fa-user"></i>
                                </el-icon>
                                <span style="font-weight: 600;">我的</span>
                            </template>
                            <router-link to="/console/userInfo">
                                <el-menu-item index="1-1">账号信息</el-menu-item>
                            </router-link>
                        </el-sub-menu>
                        <router-link to="/console/weatherDisplay">
                            <el-menu-item index="2">
                                <el-icon>
                                    <i class="fas fa-chalkboard"></i>
                                </el-icon>
                                <span style="font-weight: 600;">天气大屏</span>
                            </el-menu-item>
                        </router-link>
                        <router-link to="/console/dataDownload">
                            <el-menu-item index="3">
                                <el-icon>
                                    <i class="fas fa-download"></i>
                                </el-icon>
                                <span style="font-weight: 600;">数据下载</span>
                            </el-menu-item>
                        </router-link>
                        <router-link to="/console/temForecast">
                            <el-menu-item index="4">
                                <el-icon>
                                    <i class="fas fa-temperature-high"></i>
                                </el-icon>
                                <span style="font-weight: 600;">气温预测</span>
                            </el-menu-item>
                        </router-link>
                    </el-menu>
                    <div
                        style="text-align: center; transform: scale(0.8); bottom: 20px; position: fixed; width: 200px;">
                        <router-link class="link-fx fw-bold" to="#">
                            <i class="fas fa-cloud"></i>
                            <span class="fs-4 text-body-color">Weather Vista</span>
                        </router-link>
                    </div>

                </el-aside>
                <el-main v-loading="menuMainLoading">
                    <router-view></router-view>
                </el-main>
            </el-container>
        </el-container>
    </div>


    <!-- 公告对话框 -->
    <el-dialog v-if="false" v-model="announcementDialogVisible" title="活动通知" width="500" align-center>
        <p>本平台才开始运营两天用户人数就已经破百了，为表感谢，打算开展如下活动：</p>
        <p>在本周五（4月26日）作者会发布若干个<span style="color: red;">免费激活码</span>在<a href="https://qm.qq.com/q/O67Q2S9nKE"
                target="_blank">交流群</a>，详情可进群查看。</p>
        <p>如果没有抢到也没关系，在本周五0点至周日晚12点期间，<a href="https://afdian.net/item/2553a49e014811efafd352540025c377"
                target="_blank">商店页面</a>也会<span style="color: red;">打六折</span>，到时候也可以优惠购买。</p>
        <template #footer>
            <div class="dialog-footer">
                <el-button type="primary" @click="announcementDialogVisible = false">
                    我知道了
                </el-button>
            </div>
        </template>
    </el-dialog>

</template>

<script setup>
import { ref, getCurrentInstance, onMounted, onUnmounted } from 'vue'
import { RouterView } from 'vue-router'
import { ElLoading, ElMessage } from 'element-plus'

const asideCollapsed = ref(false)
const menuMainLoading = false
const announcementDialogVisible = ref(true)

checkLogin()
handleResize()



function handleBeforeRouteUpdate() {
    // 在子页面路由更新前将 menuMainLoading 设置为 true
    menuMainLoading.value = true
}

function checkLogin() {
    const { appContext } = getCurrentInstance()
    const access_token = localStorage.getItem('access_token')
    if (!access_token) {
        ElMessage({
            message: '请先登录',
            type: 'warning',
        })
        window.location.href = '/login'
    }
    else {
        const $serverUrl = appContext.config.globalProperties.$serverUrl
        fetch($serverUrl + '/api/checkLoginStatus', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + access_token,
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.logged_in === false) {
                    ElMessage({
                        message: '登录状态已过期，请重新登录',
                        type: 'warning',
                    })
                    window.location.href = '/login'
                } else if (data.logged_in === true) {
                    localStorage.setItem('user_info', JSON.stringify(data.user_info));
                }
            })
            .catch(error => {
                console.error('Error:', error)
                ElMessage({
                    message: '检查登陆状态失败，请重新登录',
                    type: 'warning',
                })
                window.location.href = '/login'
            })
    }
}



// 监听窗口大小变化
function handleResize() {
    if (window.innerWidth < 768) {
        asideCollapsed.value = true; // 页面宽度小于768时隐藏侧边栏
    } else {
        asideCollapsed.value = false;
    }
}

// 监听窗口大小变化事件
window.addEventListener('resize', handleResize)

// 组件销毁时移除事件监听
onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
})

function toggleCollapse() {
    asideCollapsed.value = !asideCollapsed.value
}

function userLogout() {
    // 执行退出登录操作
    // 例如发送请求到后端进行退出登录
    // 或者清除本地存储中的登录信息等

    // 示例：模拟退出登录操作，清除本地存储中的登录信息
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_info')
    // 完成后跳转到登录页面
    window.location.href = '/login'
}
</script>



<style scoped>
.collapse-btn {
    cursor: pointer;
    padding: 5px;
}
</style>