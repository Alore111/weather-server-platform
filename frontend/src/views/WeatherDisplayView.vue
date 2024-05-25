<template>
    <div class="weather-display">
        <!-- <h1 style="text-align: center;color: #333;font-size: 36px;margin-bottom: 20px;">天气大屏</h1> -->
        <!-- <div id="main" style="width: 600px;height:400px;"></div> -->
        <div class="now_display">
            <div class="block block-rounded bg-gd-dusk mb-2">
                <div class="block-content bg-white-5">
                    <div style="display: flex;justify-content: space-between;align-items: center;">
                        <h1 class="h2 fw-bold text-white mb-2">实时天气</h1>
                        <i class="h1 text-white fa-solid fa-location-dot"></i>
                        <h1 class="h2 fw-bold text-white mb-2">{{ locationText }}</h1>
                    </div>
                    <div class="py-4 text-center">
                        <i :class="'h1 text-white fa-solid qi-' + this.currentData.icon"></i>
                        <h1 class="h2 fw-bold text-white mb-2">{{ currentData.text }} {{ currentData.temp }}°C</h1>
                        <span class="text-white mb-2">云量 {{ currentData.cloud }}%</span>
                        <span class="text-info mb-2 m-2">|</span>
                        <span class="text-white mb-2">湿度 {{ currentData.humidity }}°C</span>
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
    </div>




    <el-dialog v-model="dialogLocationVisible" title="Shipping address" width="500">
        <el-form :model="form">
            <el-form-item label="Promotion name" :label-width="formLabelWidth">
                <el-input v-model="form.name" autocomplete="off" />
            </el-form-item>
            <el-form-item label="Zones" :label-width="formLabelWidth">
                <el-select v-model="form.region" placeholder="Please select a zone">
                    <el-option label="Zone No.1" value="shanghai" />
                    <el-option label="Zone No.2" value="beijing" />
                </el-select>
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="dialogLocationVisible = false">Cancel</el-button>
                <el-button type="primary" @click="dialogLocationVisible = false">
                    Confirm
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script>
import * as echarts from 'echarts'
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
            location: ''
        }
    },
    mounted() {
        // 获取天气数据
        this.updateWeatherData();
    },
    methods: {

        updateWeatherData() {
            return fetch(this.$serverUrl + `/api/weather/checkLocation?location=${this.locationText}`)
                .then(response => response.json())
                .then(data => {
                    // console.log(data);
                    if (data.code === 200) {
                        this.location_id = data.location_id;
                        this.getWeatherData(data.location_id);
                    } else {
                        alert('位置不存在');
                    }
                })
                .catch(error => console.error(error))
        },

        // 获取天气数据
        getWeatherData(location_id) {

            fetch(this.$serverUrl + `/api/weather/now?location=${location_id}`)
                .then(response => response.json())
                .then(data => {
                    this.currentData = data.data;
                    // this.currentData = Object.assign({}, data.data, {});
                })
                .catch(error => console.error(error))
        },
    },
}


</script>

<style></style>