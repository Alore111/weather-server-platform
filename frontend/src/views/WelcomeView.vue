<template>
    <div class="home_display home_background">
        <div class="row">
            <div class="col-lg-8 mb-2 home_background">
                <div class="block 24h_display" style="width: 100%; height: 37.5em;">
                    <swiper
                            :autoplay="swiperOptions.autoplay"
                            :loop="swiperOptions.loop"
                            :speed="swiperOptions.speed"
                            :pagination="swiperOptions.pagination"
                            :navigation="swiperOptions.navigation"
                            :spaceBetween="swiperOptions.spaceBetween"
                            :coverflowEffect="swiperOptions.coverflowEffect"
                            :centeredSlides="swiperOptions.centeredSlides"
                            :slidesPerView="swiperOptions.slidesPerView"
                            class="swiper"
                            effect="coverflow"
                    >

                        <swiper-slide>
                            <img class="my_swiper_imgs" src="../../public/imgs/1.jpg" alt=""/>
                        </swiper-slide>
                        <swiper-slide>
                            <img class="my_swiper_imgs" src="../../public/imgs/2.jpg" alt=""/>
                        </swiper-slide>
                        <swiper-slide>
                            <img class="my_swiper_imgs" src="../../public/imgs/3.jpg" alt=""/>
                        </swiper-slide>
                    </swiper>
                </div>
            </div>
            <div class="col-lg-4 mb-2">
                <div class="block" style="width: 100%; height: 37.5em;">
                    <div class="block-content bg-white-5">
                        <h1 class="h3 text-center fw-bold mb-2">今日高温排行</h1>
                        <router-link to="/searchWeatherByCity">
                            <el-button type="primary" :icon="Search">查看城市天气</el-button>
                        </router-link>
                        <div class="block-content bg-white-5" style="width: 100%; height: 18.75em;">
                            <el-table :data="cityTemperatures" style="width: 100%;">
                                <el-table-column prop="city" label="城市"></el-table-column>
                                <el-table-column prop="province" label="省份"></el-table-column>
                                <el-table-column prop="temperature" label="温度(℃)"></el-table-column>
                            </el-table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="now_display">
            <div class="row">

                <div class="col-lg-4 mb-2">
                    <div class="block" style="width: 100%; height: 25em;">
                        <div class="block-content bg-white-5">
                            <h1 class="h3 fw-bold text-center text-white mb-2" style="margin: 1em">气象热点</h1>
                            <div class="row">
                                <div class="col-lg-3 mb-2">
                                    <el-icon
                                            style="height:200px;width:100%;font-size:100px;color:dodgerblue">
                                        <DataLine/>
                                    </el-icon>
                                </div>
                                <div class="col-lg-9 mb-2">
                                    <el-table :data="hotSpotNewsList" style="width: 100%;">
                                        <el-table-column style="width: 100%;" prop="title">
                                            <template #default="scope">
                                                <router-link :to="'/news/' + scope.row.id">{{
                                                    scope.row.title
                                                    }}
                                                </router-link>
                                            </template>
                                        </el-table-column>
                                    </el-table>

                                </div>
                            </div>
                            <el-pagination class="custom-pagination"
                                           @size-change="handleHotSpotSizeChange"
                                           @current-change="handleHotSpotChange"
                                           :current-page="currentHotSpotPageNumber"
                                           :page-sizes="[5,10]"
                                           :page-size="currentHotSpotPageSize"
                                           layout="total, prev, pager, next, jumper"
                                           :total="currentHotSpotTotal">
                            </el-pagination>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-2">
                    <div class="block" style="width: 100%; height: 25em;">
                        <div class="block-content bg-white-5">
                            <h1 class="h3 fw-bold text-center text-white mb-2" style="margin: 1em">气象预警</h1>
                            <div class="row">
                                <div class="col-lg-3 mb-2">
                                    <el-icon
                                            style="height:200px;width:100%;font-size:100px;color:orangered">
                                        <WarnTriangleFilled/>
                                    </el-icon>
                                </div>
                                <div class="col-lg-9 mb-2">
                                    <el-table :data="alertNewsList" style="width: 100%;">
                                        <el-table-column style="width: 100%;" prop="title">
                                            <template #default="scope">
                                                <router-link :to="'/news/' + scope.row.id">{{
                                                    scope.row.title
                                                    }}
                                                </router-link>
                                            </template>
                                        </el-table-column>
                                    </el-table>

                                </div>
                            </div>
                            <el-pagination class="custom-pagination"
                                           @size-change="handleAlertSizeChange"
                                           @current-change="handleAlertChange"
                                           :current-page="currentAlertPageNumber"
                                           :page-sizes="[5,10]"
                                           :page-size="currentAlertPageSize"
                                           layout="total, prev, pager, next, jumper"
                                           :total="currentAlertTotal">
                            </el-pagination>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 mb-2">
                    <div class="block" style="width: 100%; height: 25em;">
                        <div class="block-content bg-white-5">
                            <h1 class="h3 fw-bold text-center text-white mb-2" style="margin: 1em">气象科普</h1>
                            <div class="row">
                                <div class="col-lg-3 mb-2">
                                    <el-icon
                                            style="height:200px;width:100%;font-size:100px;color:darkgreen">
                                        <Guide/>
                                    </el-icon>
                                </div>
                                <div class="col-lg-9 mb-2">
                                    <el-table :data="introductionNewsList" style="width: 100%;">
                                        <el-table-column style="width: 100%;" prop="title">
                                            <template #default="scope">
                                                <router-link :to="'/news/' + scope.row.id">{{
                                                    scope.row.title
                                                    }}
                                                </router-link>
                                            </template>
                                        </el-table-column>
                                    </el-table>

                                </div>
                            </div>
                            <el-pagination class="custom-pagination"
                                           @size-change="handleIntroductionSizeChange"
                                           @current-change="handleIntroductionChange"
                                           :current-page="currentIntroductionPageNumber"
                                           :page-sizes="[5,10]"
                                           :page-size="currentIntroductionPageSize"
                                           layout="total, prev, pager, next, jumper"
                                           :total="currentIntroductionTotal">
                            </el-pagination>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>


<script>
import {ref, reactive, onMounted} from 'vue'
import SwiperCore, {Autoplay, Pagination, EffectCoverflow, Navigation} from "swiper";
import {Swiper, SwiperSlide} from "swiper/vue";
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';
import {Search} from '@element-plus/icons-vue'


SwiperCore.use([Autoplay, Pagination, EffectCoverflow, Navigation]);


export default {
    computed: {
        Search() {
            return Search
        }
    },
    components: {
        Swiper,
        SwiperSlide,
    },
    setup() {
        const swiperOptions = reactive({
            autoplay: {
                disableOnInteraction: false, // 鼠标滑动后继续自动播放
                delay: 3000,
            },
            speed: 500, //切换过渡速度
            loop: true,
            slidesPerView: "auto", //解决最后一张切换到第一张中间的空白
            centeredSlides: true, //设置slide居中
            spaceBetween: 20,
            coverflowEffect: {
                // rotate: 0, //slide做3d旋转时Y轴的旋转角度。默认50。
                stretch: 50, //每个slide之间的拉伸值（距离），越大slide靠得越紧。 默认0。
                depth: 100, //slide的位置深度。值越大z轴距离越远，看起来越小。 默认100。
                modifier: 1, //depth和rotate和stretch的倍率，相当于            depth*modifier、rotate*modifier、stretch*modifier，值越大这三个参数的效果越明显。默认1。
            },
            // navigation: {
            //     nextElRef: ".swiper-button-next",
            //     prevElRef: ".swiper-button-prev",
            // },
            pagination: {
                clickable: true,
            },
        });

        const backgroundResources = [
            './../public/imgs/1.jpg',
            './../public/imgs/1.jpg',
            './../public/imgs/3.jpg',
            './../public/imgs/4.jpg',
            './../public/imgs/5.jpg',
            './../public/imgs/6.jpg',
            './../public/imgs/2.jpg',
            './../public/imgs/8.jpg',
        ]
        return {
            swiperOptions,
            backgroundResources
        };
    },
    name: 'WeatherDisplayView',
    data() {
        return {
            cityTemperatures: [],
            hotSpotNewsList: [],
            introductionNewsList: [],
            alertNewsList: [],

            currentHotSpotPageSize: 1,
            currentHotSpotPageNumber: 5,
            currentHotSpotTotal: 0,

            currentAlertPageSize: 1,
            currentAlertPageNumber: 5,
            currentAlertTotal: 0,

            currentIntroductionPageSize: 1,
            currentIntroductionPageNumber: 5,
            currentIntroductionTotal: 0,
        }
    },

    mounted() {
        this.getCityList()

        this.currentHotSpotPageSize = 5
        this.currentHotSpotPageNumber = 1
        const hotSportNewsData = this.getNewsList('hotSpot', this.currentHotSpotPageNumber, this.currentHotSpotPageSize)
        hotSportNewsData.then((data) => {
            this.hotSpotNewsList = data.newsList
            this.currentHotSpotTotal = data.total
        })


        this.currentAlertPageSize = 5
        this.currentAlertPageNumber = 1
        const alertNewsData = this.getNewsList('alert', this.currentAlertPageNumber, this.currentAlertPageSize)
        alertNewsData.then((data) => {
            this.alertNewsList = data.newsList
            this.currentAlertTotal = data.total
        })


        this.currentIntroductionPageSize = 5
        this.currentIntroductionPageNumber = 1
        const introductionNewsData = this.getNewsList('introduction', this.currentIntroductionPageNumber, this.currentIntroductionPageSize)
        introductionNewsData.then((data) => {
            this.currentIntroductionTotal = data.total
            this.introductionNewsList = data.newsList
        })

    },

    methods: {
        getCityList() {
            fetch(this.$serverUrl + `/api/weather/cityTemperatureRank`)
                .then(response => response.json())
                .then(result => {
                    if (result.code === 200) {
                        for (let item of result.data) {
                            this.cityTemperatures.push({
                                'city': item.city_name,
                                'province': item.province_name,
                                'temperature': item.max_temperature,
                            })
                        }
                    }
                })
                .catch(error => console.error(error))
        },

        async getNewsList(newsType, pageNumber, pageSize) {
            let currentNewsList = []
            let total = 0
            try {
                let result = await (await fetch(this.$serverUrl + `/api/weather/newsList?newsType=${newsType}&pageNumber=${pageNumber}&pageSize=${pageSize}`)).json()
                if (result.code === 200) {
                    total = result.data.total
                    for (let item of result.data.page_list) {
                        currentNewsList.push({
                            'id': item.id,
                            'title': item.title,
                        })
                    }
                }

                return {
                    'total': total,
                    'newsList': currentNewsList
                }
            } catch (error) {
                console.log('Request Failed', error);
            }


        },
        handleHotSpotSizeChange(pageSize) {
            this.currentHotSpotPageSize = pageSize
            const newsListData = this.getNewsList('hotSpot', this.currentHotSpotPageNumber, this.currentHotSpotPageSize)
            newsListData.then((data) => {
                this.hotSpotNewsList = data.newsList
                this.currentHotSpotTotal = data.total
            })

        },
        handleHotSpotChange(pageNumber) {
            this.currentHotSpotPageNumber = pageNumber
            const newsListData = this.getNewsList('hotSpot', this.currentHotSpotPageNumber, this.currentHotSpotPageSize)
            newsListData.then((data) => {
                this.hotSpotNewsList = data.newsList
                this.currentHotSpotTotal = data.total
            })
        },
        handleAlertSizeChange(pageSize) {
            this.currentAlertPageSize = pageSize
            const newsListData = this.getNewsList('alert', this.currentAlertPageNumber, this.currentAlertPageSize)
            newsListData.then((data) => {
                this.alertNewsList = data.newsList
                this.currentAlertTotal = data.total
            })

        },
        handleAlertChange(pageNumber) {
            this.currentAlertPageNumber = pageNumber
            const newsListData = this.getNewsList('alert', this.currentAlertPageNumber, this.currentAlertPageSize)
            newsListData.then((data) => {
                this.alertNewsList = data.newsList
                this.currentAlertTotal = data.total
            })
        },
        handleIntroductionSizeChange(pageSize) {
            this.currentIntroductionPageSize = pageSize
            const newsListData = this.getNewsList('introduction', this.currentIntroductionPageNumber, this.currentIntroductionPageSize)
            newsListData.then((data) => {
                this.introductionNewsList = data.newsList
                this.currentIntroductionTotal = data.total
            })

        },
        handleIntroductionChange(pageNumber) {
            this.currentIntroductionPageNumber = pageNumber
            const newsListData = this.getNewsList('introduction', this.currentIntroductionPageNumber, this.currentIntroductionPageSize)
            newsListData.then((data) => {
                this.introductionNewsList = data.newsList
                this.currentIntroductionTotal = data.total
            })
        },

    },
}

</script>
<style>
.home_display {
    padding: 10px;
    border-radius: 10px;
}

.block {
    padding: 10px;
    border-radius: 10px;
    box-shadow: none;
}

.block-content {
    padding: 10px;
    border-radius: 10px;
}

.h2 {
    color: #ecf0f1;
}

.text-white {
    color: #000000 !important;
}

.text-info {
    color: #3498db !important;
}

.my_swiper_imgs {
    height: 35em;
    width: 100%;
}

a {
    color: inherit;
}

.custom-pagination {
    margin-top: 1em
}

</style>
