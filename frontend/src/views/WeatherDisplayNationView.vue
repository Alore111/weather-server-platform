<template>
    <div class="weather-map">
        <div ref="mapContainer" class="map-container"></div>
    </div>
</template>

<script>
export default {
    name: 'WeatherMap',
    data() {
        return {
            map: null,
            labelsLayer: null,
            weatherData: [],
            currentZoomRange: 'low', // 当前缩放区间
        };
    },
    mounted() {
        this.initMap();
        this.fetchWeatherData();
    },
    methods: {
        initMap() {
            this.map = new AMap.Map(this.$refs.mapContainer, {
                zoom: 5,
                center: [105.397428, 36.870723],
                viewMode: '3D',
                mapStyle: 'amap://styles/blue',
                features: ['bg', 'road', 'point'],
                showIndoorMap: false,
                showLabel: false,
            });

            this.labelsLayer = new AMap.LabelsLayer({
                zooms: [3, 20],
                zIndex: 1000,
                collision: false,
                allowCollision: false,
            });

            this.map.add(this.labelsLayer);

            this.map.on('zoomend', this.handleZoomChange);
        },
        fetchWeatherData() {
            fetch(this.$serverUrl + '/api/weather/nationwide')
                .then(response => response.json())
                .then(data => {
                    if (data.code === 200) {
                        this.weatherData = data.data.city;


                        // let zoomLevel = this.map.getZoom();
                        // let newZoomRange = this.getZoomRange(zoomLevel);

                        // this.currentZoomRange = newZoomRange;

                        // // 根据权重过滤数据
                        // let filteredData = data.data.city.filter(city => {
                        //     if (newZoomRange === 'low') {
                        //         return city[3] < 2; // 示例阈值
                        //     } else if (newZoomRange === 'medium') {
                        //         return city[3] < 3; // 示例阈值
                        //     } else {
                        //         return city[3] < 4; // 示例阈值
                        //     }
                        // });

                        // console.log(filteredData)
                        // console.log(data.data.city)

                        // 添加所有标签
                        this.addLabels();
                        
                        // // 清除所有标签
                        // this.labelsLayer.clear();

                        // // 添加过滤后的标签
                        // this.addLabels(filteredData);

                        // this.handleZoomChange();
                    } else {
                        alert('获取天气数据失败');
                    }
                })
                .catch(error => console.error('Error fetching weather data:', error));
        },
        addLabels(filteredData = this.weatherData) {
            const markers = [];

            const getColorByTemperature = (temp) => {
                // if (temp < 0) return '#00BFFF';          // DeepSkyBlue
                // // if (temp < 5) return '#1E90FF';           // DodgerBlue
                // if (temp < 10) return '#87CEFA';          // LightSkyBlue
                // // if (temp < 15) return '#00FF7F';          // SpringGreen
                // if (temp < 20) return '#32CD32';          // LimeGreen
                // // if (temp < 25) return '#ADFF2F';          // GreenYellow
                // if (temp < 30) return '#FFD700';          // Gold
                // // if (temp < 35) return '#FFA500';          // Orange
                // if (temp < 40) return '#FF4500';          // OrangeRed
                // return '#FF0000';                         // Red

                if (temp < 10) return '#3d9df6';
                if (temp < 20) return '#6cbd40';
                if (temp < 30) return '#f5a54f';
            };

            const openInfoWindow = (city) => {

                let infoCity = city[1];

                let infoWeather = city[7];
                if (city[7] != city[12]) {
                    infoWeather = city[7] + '转' + city[12];
                }

                let infoWeatherImg = city[8];
                let infoTemperature = city[6] + ' / ' + city[11] + '°C';
                let infoWindDirection = city[9];
                let infoWindPower = city[10];
                let infoWind = (infoWindDirection == '无持续风向' ? '' : infoWindDirection + ' ') + infoWindPower;



                // 创建信息窗体的内容
                const content = `
                    <div class="info-window">
                        <p style="line-height:70px; font-size: 20px; font-weight: 600; color: #c4e1f7"> ${infoCity} <img style="width: 50px;" src="https://weather.cma.cn/static/img/w/icon/w${infoWeatherImg}.png" /></p>
                        <p><strong>温度:</strong> ${infoTemperature}</p>
                        <p><strong>天气:</strong> ${infoWeather}</p>
                        <p><strong>风:</strong> ${infoWind}</p>
                    </div>
                `;
                // 创建信息窗体并打开
                const infoWindow = new AMap.InfoWindow({
                    content: content,
                    position: [city[5], city[4]],
                });
                infoWindow.open(this.map, [city[5], city[4]]);
            };

            filteredData.forEach(city => {
                const color = getColorByTemperature(city[11]);
                const textStyle = {
                    fontSize: 12,
                    fontWeight: 'normal',
                    fillColor: '#fff',
                    backgroundColor: color,
                    borderColor: '#fff',
                    borderWidth: 1,
                    padding: '2, 5',
                };

                const marker = new AMap.LabelMarker({
                    name: city[1],
                    position: [city[5], city[4]],
                    zIndex: city[11],
                    text: {
                        content: `${city[1]}: ${city[11]}°C, ${city[10]}`,
                        direction: 'center',
                        style: textStyle,
                    }
                });

                marker.on('click', () => {
                    // 点击标签时打开信息窗体
                    openInfoWindow(city);
                });

                markers.push(marker);
            });
            console.log("addedMarkers,",markers)
            this.labelsLayer.add(markers);
        },
        getZoomRange(zoomLevel) {
            if (zoomLevel < 6.3) return 'low';
            if (zoomLevel < 8.5) return 'medium';
            return 'high';
        },
        handleZoomChange() {
            const zoomLevel = this.map.getZoom();
            const newZoomRange = this.getZoomRange(zoomLevel);

            // console.log('Zoom level changed:', zoomLevel);
            // console.log('Zoom range:', newZoomRange);

            // 只有在缩放区间发生变化时才重新渲染点
            if (newZoomRange !== this.currentZoomRange) {
                // console.log('Zoom range changed, re-rendering points...');
                this.currentZoomRange = newZoomRange;

                // 清除所有标签
                this.labelsLayer.clear();

                // 根据权重过滤数据
                const filteredData = this.weatherData.filter(city => {
                    if (newZoomRange === 'low') {
                        return city[3] < 2; // 示例阈值
                    } else if (newZoomRange === 'medium') {
                        return city[3] < 3; // 示例阈值
                    } else {
                        return city[3] < 4; // 示例阈值
                    }
                });

                // 添加过滤后的标签
                this.addLabels(filteredData);
            }
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
    height: 90vh;
    background-color: #2c3e50;
}

.info-window {
    font-family: Arial, sans-serif;
    font-size: 14px;
    line-height: 1.6;
    color: #fff;
    padding: 10px;
    /* background-color: #fff; */
}

.amap-info-content {
    background: #2b536b;
}

.info-window p {
    margin: 5px 0;
}

.info-window strong {
    font-weight: bold;
}
</style>
