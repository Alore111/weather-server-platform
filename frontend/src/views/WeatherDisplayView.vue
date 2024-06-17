<template>
    <div class="weather-display">
        <div class="now_display">
            <div class="block block-rounded mb-2">
                <div class="block-content bg-white-5">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h1 class="h2 fw-bold text-white mb-2">实时天气</h1>
                        <i class="h1 text-white fa-solid fa-location-dot"></i>
                        <h1 class="h2 fw-bold text-white mb-2" style="cursor: pointer;"
                            @click="this.dialogLocationVisible = true;">
                            <i class="fas fa-house-user"></i> {{ locationText }}
                        </h1>
                    </div>
                    <div class="py-4 text-center">
                        <i :class="'h1 text-white fa-solid qi-' + this.currentData.icon"></i>
                        <h1 class="h2 fw-bold text-white mb-2">{{ currentData.text }} {{ currentData.temp }}°C</h1>
                        <span class="text-white mb-2">云量 {{ currentData.cloud }}%</span>
                        <span class="text-info mb-2 m-2">|</span>
                        <span class="text-white mb-2">湿度 {{ currentData.humidity }}%</span>
                        <span class="text-info mb-2 m-2">|</span>
                        <span class="text-white mb-2">体感温度 {{ currentData.feelsLike }}°C</span>
                        <span class="text-info mb-2 m-2">|</span>
                        <span class="text-white mb-2">能见度 {{ currentData.vis }}km</span>
                        <span class="text-info mb-2 m-2">|</span>
                        <span class="text-white mb-2">风速 {{ currentData.windSpeed }}m/s {{ currentData.windDir }}</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-lg-8 mb-2">
                <div class="block 24h_display" style="width: 100%; height: 400px;" ref="chartContainer"></div>
            </div>
            <div class="col-lg-4 mb-2">
                <div class="block" style="width: 100%; height: 400px;">
                    <div class="block-content bg-white-5">
                        <h1 class="h3 text-center fw-bold text-white mb-2">全国天气地图</h1>
                        <div class="block-content bg-white-5" style="width: 100%; height: 300px;">

                            <router-link to="/console/weatherDisplayNation">
                                <h2 class="py-7 text-center fw-bold text-white mb-2">点击查看</h2>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <el-dialog v-model="dialogLocationVisible" title="切换地区" width="500">
            <el-form-item label="市/区/县" :label-width="formLabelWidth">
                <el-input v-model="locationTextTemp" autocomplete="off" />
            </el-form-item>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="dialogLocationVisible = false">取消</el-button>
                    <el-button type="primary" @click="dialogLocationVisible = false; this.updateWeatherData();">
                        确定
                    </el-button>
                </div>
            </template>
        </el-dialog>
    </div>
</template>


<script>
import * as echarts from 'echarts'
import { ref } from 'vue'
import { ElButton, ElDialog, ElForm, ElFormItem, ElInput } from 'element-plus'
import router from '@/router'

export default {
    name: 'WeatherDisplayView',
    data() {
        return {
            currentData: {
                cloud: null,
                dew: null,
                feelsLike: null,
                humidity: null,
                icon: null,
                obsTime: null,
                precip: null,
                pressure: null,
                temp: null,
                text: null,
                vis: null,
                wind360: null,
                windDir: null,
                windScale: null,
                windSpeed: null,
            },
            dialogLocationVisible: false,
            temp: 0,
            locationText: '双流',
            locationTextTemp: '双流',
            location: '',
            chart: null,
        }
    },
    mounted() {
        // 初始化图表
        this.chart = echarts.init(this.$refs.chartContainer);
        this.updateWeatherData();
    },
    methods: {
        updateWeatherData() {
            return fetch(this.$serverUrl + `/api/weather/checkLocation?location=${this.locationTextTemp}`)
                .then(response => response.json())
                .then(data => {
                    if (data.code === 200) {
                        this.locationText = this.locationTextTemp;
                        this.location_id = data.location_id;
                        this.getWeatherData(data.location_id);
                    } else {
                        alert('位置不存在');
                    }
                })
                .catch(error => console.error(error))
        },
        getWeatherData(location_id) {
            fetch(this.$serverUrl + `/api/weather/now?location=${location_id}`)
                .then(response => response.json())
                .then(data => {
                    this.currentData = data.data;
                    this.get24hWeatherData(location_id);
                })
                .catch(error => console.error(error))
        },
        get24hWeatherData(location_id) {
            fetch(this.$serverUrl + `/api/weather/24h?location=${location_id}`)
                .then(response => response.json())
                .then(data => {
                    if (data.code === 200) {
                        this.renderChart(data.data);
                    }
                })
                .catch(error => console.error(error))
        },
        renderChart(data) {
            const times = data.map(item => item.fxTime.substring(11, 16));
            const temps = data.map(item => item.temp);
            const humidities = data.map(item => item.humidity);
            const winds = data.map(item => item.windSpeed);

            const option = {
                title: {
                    text: '24小时天气预报',
                    left: 'center',
                    textStyle: {
                        color: '#fff',
                    },
                },
                tooltip: {
                    trigger: 'axis',
                },
                legend: {
                    data: ['温度', '湿度', '风速'],
                    top: '10%',
                    textStyle: {
                        color: '#fff',
                    },
                },
                xAxis: {
                    type: 'category',
                    data: times,
                    axisLine: {
                        lineStyle: {
                            color: '#fff',
                        },
                    },
                },
                yAxis: [
                    {
                        type: 'value',
                        name: '温度 (°C)',
                        position: 'left',
                        axisLine: {
                            lineStyle: {
                                color: '#fff',
                            },
                        },
                        axisLabel: {
                            formatter: '{value} °C',
                        },
                    },
                    {
                        type: 'value',
                        name: '湿度 (%)',
                        position: 'right',
                        axisLine: {
                            lineStyle: {
                                color: '#fff',
                            },
                        },
                        axisLabel: {
                            formatter: '{value} %',
                        },
                    },
                    {
                        type: 'value',
                        name: '风速 (m/s)',
                        position: 'right',
                        offset: 60,
                        axisLine: {
                            lineStyle: {
                                color: '#fff',
                            },
                        },
                        axisLabel: {
                            formatter: '{value} m/s',
                        },
                    },
                ],
                series: [
                    {
                        name: '温度',
                        type: 'line',
                        data: temps,
                    },
                    {
                        name: '湿度',
                        type: 'line',
                        yAxisIndex: 1,
                        data: humidities,
                    },
                    {
                        name: '风速',
                        type: 'line',
                        yAxisIndex: 2,
                        data: winds,
                    },
                ],
            };
            this.chart.setOption(option);
        },
    },
}

</script>
<style>
.weather-display {
    background-color: #2c3e50;
    padding: 20px;
    border-radius: 10px;
}

.weather-display .block {
    background-color: #34495e;
    padding: 20px;
    border-radius: 10px;
    box-shadow: none;
}

.block-content {
    background-color: #2c3e50;
    padding: 20px;
    border-radius: 10px;
}

.h2 {
    color: #ecf0f1;
}

.text-white {
    color: #ecf0f1 !important;
}

.text-info {
    color: #3498db !important;
}
</style>
