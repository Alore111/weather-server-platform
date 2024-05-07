<template>
  <div id="page-container" class="sidebar-dark side-scroll page-header-fixed page-header-glass main-content-boxed">
    <!-- Header -->
    <header id="page-header">
      <div class="content-header">
        <div class="space-x-1">
          <router-link class="link-fx fw-bold" :to="{ path: '/' }">
            <i class="fas fa-wind" style="color:#fff"></i>
            <span class="fs-4" style="color:#fff">Weather Vista</span>
          </router-link>
        </div>
        <div class="d-flex align-items-center space-x-2">
          <ul class="nav-main nav-main-horizontal nav-main-hover d-none d-lg-block">
            <li class="nav-main-item">
              <router-link class="nav-main-link active" :to="{ path: '/' }">
                <i class="nav-main-link-icon fa fa-home" style="color: #fff;"></i>
                <span class="nav-main-link-name" style="color: #fff;">首页</span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
      <div class="overlay-header bg-primary" id="page-header-loader">
        <div class="content-header">
          <div class="w-100 text-center">
            <i class="far fa-sun fa-spin text-white"></i>
          </div>
        </div>
      </div>
    </header>
    <!-- Main Content -->
    <main id="main-container" style="margin-top: 68px;">
      <div class="main-inner-container">
        <div class="main-left">
          <h1>Weather Vista</h1>
          <p>介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍介绍</p>
        </div>
        <div class="main-right">
        </div>
      </div>
    </main>
    <!-- Footer -->
    <footer class="bg-body-extra-light" id="page-footer">
      <div class="content content-full">
        <div class="row g-0 fs-sm border-top pt-3">
          <div class="col-sm-6 order-sm-2 py-1 text-center text-sm-end">
            &copy; <span data-toggle="year-copy"></span> <a class="fw-semibold" href="#" target="_blank">Weather Vista</a>
          </div>
          <div class="col-sm-6 order-sm-1 py-1 text-center text-sm-start">
            <a href="https://beian.miit.gov.cn/" target="_blank" class="text-muted fw-semibold"></a>
          </div>
        </div>
      </div>
    </footer>
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


#page-container.page-header-glass #page-header {
    position: absolute;
    background-color: #1A62FF;
}

.main-left {
    width: 30%;
    height: 100%;
    /* 其他样式 */
    display: flex;
    justify-content: center;
    align-items: center;
}

.main-right {
    width: 70%;
    height: 100%;
    /* 其他样式 */
}

.main-inner-container {
    display: flex;
    justify-content: space-between;
}
</style>
