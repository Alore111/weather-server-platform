<template>
  <div id="page-container" class="sidebar-dark side-scroll page-header-fixed page-header-glass main-content-boxed">
    <!-- Sidebar -->
    <nav id="sidebar">
      <div class="sidebar-content">
        <div class="content-header justify-content-lg-center bg-black-10">
          <div>
            <span class="smini-visible fw-bold tracking-wide fs-lg">
              o<span class="text-primary">t</span>
            </span>
            <router-link class="link-fx fw-bold tracking-wide mx-auto" :to="{ path: '/' }">
              <span class="smini-hidden">
                <i class="fas fa-cloud"></i>
                <span class="fs-4 text-dual">Weather Vista</span>
              </span>
            </router-link>
          </div>
          <div>
            <button class="btn btn-sm btn-alt-danger d-lg-none" @click="closeSidebar" type="button">
              <i class="fa fa-fw fa-times"></i>
            </button>
          </div>
        </div>
        <div class="js-sidebar-scroll">
          <div class="content-side content-side-full">
            <ul class="nav-main">
              <li class="nav-main-item">
                <router-link class="nav-main-link active" :to="{ path: '/' }">
                  <i class="nav-main-link-icon fa fa-home"></i>
                  <span class="nav-main-link-name">首页</span>
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
    <!-- Header -->
    <header id="page-header">
      <div class="content-header">
        <div class="space-x-1">
          <router-link class="link-fx fw-bold" :to="{ path: '/' }">
            <i class="fas fa-cloud"></i>
            <span class="fs-4" style="color: #454C53;">Weather Vista</span>
          </router-link>
        </div>
        <div class="d-flex align-items-center space-x-2">
          <ul class="nav-main nav-main-horizontal nav-main-hover d-none d-lg-block">
            <li class="nav-main-item">
              <router-link class="nav-main-link active" :to="{ path: '/console' }">
                <i class="nav-main-link-icon fas fa-terminal"></i>
                <span class="nav-main-link-name" style="color: #454C53;">控制台</span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
      <div class="overlay-header bg-primary" id="page-header-loader">
        <div class="content-header">
          <div class="w-100 text-center">
            <i class="far fa-sun fa-spin text-info"></i>
          </div>
        </div>
      </div>
    </header>
    <!-- Main Content -->
    <main id="main-container">
      <div class="bg-body-extra-light overflow-hidden bg-image"
        :style="{ 'background-image': 'url(https://cdnjson.com/images/2024/05/14/clouds-1282314_19204a2556ad63d1149c.jpg)' }" id="home">
        <div class="hero">
          <div class="hero-inner">
            <div class="content content-full text-center">
              <h1 class="display-3 fw-bold text-info mb-2">Weather Vista</h1>
              <h4 class="fw-medium text-info-50 mb-5">天气服务系统</h4>
              <a class="btn btn-lg btn-alt-info fw-semibold me-1 mb-2 fs-sm" href="/login">
                <i class="fas fa-sign-in-alt opacity-50 me-1"></i> 登 录
              </a>
              <a class="btn btn-lg btn-primary fw-semibold me-1 mb-2 fs-sm" href="/register">
                <i class="fab fa-google-drive opacity-50 me-1"></i> 注 册
              </a>
              <a class="btn btn-lg btn-secondary fw-semibold mb-2 fs-sm" href="/console">
                <i class="nav-main-link-icon fas fa-terminal opacity-50"></i> 控制台
              </a>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  methods: {
    closeSidebar() {
      // 关闭侧边栏逻辑
    },
    changeTheme(theme) {
      // 更改主题逻辑
    }
  }
}
</script>

<style scoped>
/* 样式表 */
</style>
