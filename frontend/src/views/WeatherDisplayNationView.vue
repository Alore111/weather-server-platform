<template>
    <div class="weather-map">
        <div ref="mapContainer" class="map-container"></div>
    </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
    name: 'WeatherMap',
    data() {
        return {
            mapChart: null,
            weatherData: [],
        };
    },
    mounted() {
        this.mapChart = echarts.init(this.$refs.mapContainer);
        this.fetchChinaMapData();
    },
    methods: {
        fetchChinaMapData() {
            fetch('/china.json')
                .then(response => response.json())
                .then(chinaJson => {
                    echarts.registerMap('china', chinaJson);
                    this.fetchWeatherData();
                })
                .catch(error => console.error('Error fetching China map data:', error));
        },
        fetchWeatherData() {
            fetch(this.$serverUrl + '/api/weather/nationwide')
                .then(response => response.json())
                .then(data => {
                    if (data.code === 200) {
                        this.weatherData = data.data.city;
                        this.renderMap();
                    } else {
                        alert('获取天气数据失败');
                    }
                })
                .catch(error => console.error('Error fetching weather data:', error));
        },
        filterVisiblePoints(points, boundingRect) {
            return points.filter(point => {
                const [lng, lat] = point.value;
                return (
                    lng >= boundingRect.x &&
                    lng <= boundingRect.x + boundingRect.width &&
                    lat >= boundingRect.y &&
                    lat <= boundingRect.y + boundingRect.height
                );
            });
        },
        renderMap() {
            const seriesData = this.weatherData.map(city => ({
                name: city[1],
                value: [city[5], city[4], city[10], city[11]], // 经度, 纬度, 温度, 天气描述
            }));

            const option = {
                title: {
                    text: '全国天气地图',
                    left: 'center',
                    textStyle: {
                        color: '#fff',
                    },
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function (params) {
                        return `${params.name}<br/>温度: ${params.value[3]}°C<br/>风: ${params.value[2]}`;
                    },
                },
                geo: {
                    map: 'china',
                    roam: true,
                    label: {
                        show: true,
                        color: '#fff',
                    },
                    itemStyle: {
                        areaColor: '#323c48',
                        borderColor: '#111',
                    },
                    emphasis: {
                        label: {
                            show: true,
                        },
                        itemStyle: {
                            areaColor: '#2a333d',
                        },
                    },
                },
                series: [
                    {
                        name: '城市天气',
                        type: 'scatter',
                        coordinateSystem: 'geo',
                        data: seriesData, // 初始渲染时不进行过滤
                        symbolSize: 10,
                        label: {
                            show: false,
                        },
                        itemStyle: {
                            color: '#ddb926',
                        },
                        emphasis: {
                            label: {
                                show: true,
                                formatter: function (params) {
                                    return `${params.name}\n温度: ${params.value[2]}°C\n天气: ${params.value[3]}`;
                                },
                                position: 'right',
                                color: '#fff',
                            },
                        },
                    },
                ],
            };

            this.mapChart.setOption(option);

            this.mapChart.on('georoam', () => {
                const geo = this.mapChart.getModel().getComponent('geo').coordinateSystem;
                const boundingRect = geo.getViewRect().clone().applyTransform(geo.transform);
                const visibleData = this.filterVisiblePoints(seriesData, boundingRect);
                const option = this.mapChart.getOption();
                option.series[0].data = visibleData;
                this.mapChart.setOption(option);
            });

            // Initial rendering of visible points
            const geo = this.mapChart.getModel().getComponent('geo').coordinateSystem;
            const boundingRect = geo.getViewRect().clone().applyTransform(geo.transform);
            const visibleData = this.filterVisiblePoints(seriesData, boundingRect);
            option.series[0].data = visibleData;
            this.mapChart.setOption(option);
        },
    },
};
</script>

<style>
.weather-map {
    width: 100%;
    height: 100%;
}

.map-container {
    width: 100%;
    height: 100vh;
    /* 设置高度 */
    background-color: #2c3e50;
}
</style>
