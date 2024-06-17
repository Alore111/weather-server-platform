import { createRouter, createWebHistory } from 'vue-router'
import NProgress from 'nprogress' 
import 'nprogress/nprogress.css'// nprogress样式文件

// 个性化配置进度条外观
NProgress.configure({
  easing: 'ease',  // 动画方式    
  speed: 500,  // 递增进度条的速度    
  showSpinner: false, // 是否显示加载ico    
  trickleSpeed: 200, // 自动递增间隔    
  minimum: 0.3 // 初始化时的最小百分比
})

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home-start',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/find',
      name: 'find',
      component: () => import('../views/FindView.vue')
    },
    {
      path: '/reset',
      name: 'reset',
      component: () => import('../views/ResetPasswordView.vue')
    },
    {
      path: '/console',
      name: 'console',
      component: () => import('../views/ConsoleView.vue'),
      children: [
        {
          path: '',
          name: 'console-console',
          component: () => import('../views/WelcomeView.vue')
        },
        {
          path: 'about',
          name: 'console-about',
          component: () => import('../views/AboutView.vue')
        },
        {
          path: 'userInfo',
          name: 'console-userInfo',
          component: () => import('../views/UserInfoView.vue')
        },
        {
          path: 'weatherDisplay',
          name: 'console-weatherDisplay',
          component: () => import('../views/WeatherDisplayView.vue')
        },
        {
          path: 'weatherDisplayNation',
          name: 'console-weatherDisplayNation',
          component: () => import('../views/WeatherDisplayNationView.vue')
        },
        {
          path: 'dataDownload',
          name: 'console-dataDownload',
          component: () => import('../views/DataDownloadView.vue')
        },
        {
          path: 'temForecast',
          name: 'console-temForecast',
          component: () => import('../views/TemForecastView.vue')
        },
        {
          path: 'adminUser',
          name: 'console-adminUser',
          component: () => import("../views/AdminUser.vue")
        },
        {
          path: '/searchWeatherByCity',
          name: 'searchWeatherByCity',
          component: () => import('../views/migrate/Home/HomeView.vue')
        }, {
          path: "/city",
          component: () => import("../views/migrate/City/City.vue")
        }, {
          path: "/weather",
          component: () => import("../views/migrate/Home/components/Weather.vue")
        }, {
          path: '/news/:id',
          component: () => import("../views/NewsDetail.vue")
        }, 
      ]
    }
  ]
})

//当路由开始跳转时
router.beforeEach((to, from , next) => {
  // 开启进度条
  NProgress.start();
  // 这个一定要加，没有next()页面不会跳转的。这部分还不清楚的去翻一下官网就明白了
  next();
});
//当路由跳转结束后
router.afterEach(() => {  
  // 关闭进度条
  NProgress.done()
})

export default router
