<template>
    <div class="weather-display">
        <div class="now_display">
            <div class="block block-rounded mb-2">
                <div class="block-content bg-white-5">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h1 class="h2 fw-bold text-white mb-2">{{getNewsTypeDesc(news.newsType)}}</h1>
                        <i class="h1 text-white fa-solid fa-location-dot"></i>
                    </div>
                    <div class="py-4 text-center">
                        <h1 class="h2 fw-bold text-white mb-2">{{ news.title }}</h1>
                        <span class="text-white mb-2">发布人: {{ news.creator }}</span>
                        <span class="text-info mb-2 m-2">|</span>
                        <span class="text-white mb-2">发布时间: {{ news.createdDatetime }}</span>
                        <span class="text-info mb-2 m-2">|</span>
                        <span class="text-white mb-2">阅读量 {{ news.readCount }}次</span>
                    </div>
                    <hr>
                    <div class="block 24h_display" style="width: 100%; height: 600px;">
                       {{news.content}}
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>


<script>
export default {
    name: 'WeatherDisplayView',
    data() {
        return {
            news: {},
        }
    },
    mounted() {
        const newsId = this.$route.params.id;
        console.log(newsId)
        this.getCityList(newsId)
    },
    methods: {
        getNewsTypeDesc(newsType) {
            if(newsType === 'hotSpot') {
                return '气象热点'
            } else if(newsType === 'alert') {
                return '天气预警'
            } else {
                return '天气科普'
            }
        },
        convertGmtTime(time) {
            let date = new Date(time)
            return date.getFullYear() + '-' +
                (date.getMonth() + 1) + '-' +
                date.getDate() + ' ' +
                date.getHours() + ':' +
                date.getMinutes()
        },
        getCityList(newsId) {
            fetch(this.$serverUrl + `/api/weather/news?id=${newsId}`)
                .then(response => response.json())
                .then(result => {
                    if (result.code === 200) {
                        this.news = {
                            'title': result.data.title,
                            'creator': result.data.creator,
                            'createdDatetime': this.convertGmtTime(result.data.createdDatetime),
                            'newsType': result.data.type,
                            'content': result.data.content,
                            'readCount': result.data.readCount,
                        }
                    }
                })
                .catch(error => console.error(error))
        },

    },
}

</script>
<style>
.weather-display {
    /*background-color: #2c3e50;*/
    padding: 20px;
    border-radius: 10px;
}

.block {
    /*background-color: #34495e;*/
    padding: 20px;
    border-radius: 10px;
    box-shadow: none;
}

.block-content {
    /*background-color: #2c3e50;*/
    padding: 20px;
    border-radius: 10px;
}

.h2 {
    color: #000000;
}

.text-white {
    color: #000000 !important;
}

.text-info {
    /*color: #3498db !important;*/
}
</style>
