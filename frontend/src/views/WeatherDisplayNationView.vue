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
            markers: [],
            weatherData: [],
            markerCluster: null,
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
                mapStyle: 'amap://styles/blue',
            });

            AMap.plugin(['AMap.MarkerClusterer'], () => {
                this.markerCluster = new AMap.MarkerClusterer(this.map, [], {
                    gridSize: 80,
                    minClusterSize: 2,
                });
            });

            this.map.on('zoomend', this.handleZoomChange);
        },
        fetchWeatherData() {
            fetch(this.$serverUrl + '/api/weather/nationwide')
            // fetch('https://weather.cma.cn/api/map/weather/1')
                .then(response => response.json())
                .then(data => {
                    if (data.code === 200) {
                        this.weatherData = data.data.city;
                        this.addMarkers();
                    } else {
                        alert('获取天气数据失败');
                    }
                })
                .catch(error => console.error('Error fetching weather data:', error));
        },
        addMarkers() {
            this.clearMarkers();

            this.weatherData.forEach(city => {
                const marker = new AMap.Marker({
                    position: [city[5], city[4]],
                    title: `${city[1]}: ${city[11]}°C, ${city[10]}`,
                    map: this.map,
                });

                marker.content = `${city[1]}<br/>温度: ${city[11]}°C<br/>风: ${city[10]}`;
                marker.on('click', this.markerClick);

                this.markers.push(marker);
            });

            this.markerCluster.addMarkers(this.markers);
        },
        markerClick(e) {
            const infoWindow = new AMap.InfoWindow({
                content: e.target.content,
                offset: new AMap.Pixel(0, -30),
            });
            infoWindow.open(this.map, e.target.getPosition());
        },
        clearMarkers() {
            // this.markerCluster.clearMap();
            this.markers = [];
        },
        handleZoomChange() {
            const zoomLevel = this.map.getZoom();
            if (zoomLevel < 7) {
                this.markerCluster.setMinClusterSize(5);
            } else {
                this.markerCluster.setMinClusterSize(2);
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
    height: 100vh;
    background-color: #2c3e50;
}
</style>
