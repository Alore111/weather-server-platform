<template>
    <div>


        <div>
            <el-upload
               
                class="upload-demo"
                :action="this.$serverUrl + '/upload'"
                drag
            
                :on-success="uploadSuccess"
                :show-file-list="false"
                :limit="1"
                
            >

            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
                支持点击/粘贴/拖拽到此区域上传，支持选择多个文件/文件夹
                <br />
                单个文件夹最大支持10M
      
            </div>
                <template #tip>
                <!-- <div class="el-upload__tip">
                    支持点击/粘贴/拖拽到此区域上传，支持选择多个文件/文件夹
                <br />
                单个文件夹最大支持10M
                </div> -->
                </template>
            </el-upload>
        </div>

        <div class="info-box" v-if="show">
            <p>关于本模型：长短期记忆（LSTM）网络的时间序列预测模型，通过多个LSTM 层以及全连接层的堆叠，有效地学习了时间序列数据的复杂模式和特征，使得模型能够对未来的气温进行准确的预测。</p>
            <p class="yanse">注意：文件格式为csv</p>
        </div>
        
        <div v-else style="text-align: right;margin: 5px 0;">
            <a :href="this.$serverUrl + '/static/predictions.csv'">预测文件下载</a>
        </div>
        
        <div id="main" style="width: 80vw;height: 350px;margin: auto;"></div>
    </div>
</template>
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts';

const upload = ref(null)
const active = ref(false)
const fileIpt = ref(null)
const show = ref(true)
defineProps(['accept'])
const handleMouseover = function (event) {
    fileIpt.value.focus()
    // 粘贴
    fileIpt.value.addEventListener('paste', handlePaste)
}
const handleMouseout = function (event) {
    fileIpt.value.blur()
    fileIpt.value.removeEventListener('paste', handlePaste)
}
onMounted(() => {
    // 拖拽
    // upload.value.addEventListener('drop', handleDrop)
    // upload.value.addEventListener('dragleave', handleDragleave)
    // upload.value.addEventListener('dragenter', handleDragenter)
    // upload.value.addEventListener('dragover', handleDragenter)
    // upload.value.addEventListener('mouseover', handleMouseover);
    // upload.value.addEventListener('mouseout', handleMouseout);
})
 
onUnmounted(() => {
    // upload.value.removeEventListener('drop', handleDrop)
    // upload.value.removeEventListener('dragleave', handleDragleave)
    // upload.value.removeEventListener('dragenter', handleDragenter)
    // upload.value.removeEventListener('dragover', handleDragenter)
    // upload.value.removeEventListener('mouseover', handleMouseover);
    // upload.value.removeEventListener('mouseout', handleMouseout);
})
 
const emit = defineEmits(["file"])
const handleFileName = (fileList) => {
    let files = Array.from(fileList)
    let renameReportFile = []
    for (let i in files) {
        renameReportFile.push(new File([files[i]], new Date().getTime() + files[i].name, { type: files[0].type }))
    }
    emit("file", renameReportFile)
}
const changeFile = (e) => {
    e.preventDefault()
    handleFileName(e.target.files)
}
 
const handleDragleave = (e) => {
    active.value = false
    e.preventDefault()
}
const handleDragenter = (e) => {
    active.value = true
    e.preventDefault()
}
 
const handleDrop = (e) => {
    e.preventDefault()
    active.value = false
    handleFileName(e.dataTransfer.files)
}
 
const handlePaste = (e) => {
    e.preventDefault()
    handleFileName(e.clipboardData.files)
}

function uploadSuccess(res){
console.log(res);
keshihua(res['data'])
}


function keshihua(data) {


var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option;
show.value = false;

option = {
  title: {
    text: '气温预测'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['原始数据', '预测值', ]
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  toolbox: {
    feature: {
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: data['date']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    
    
    {
      name: '原始数据',
      type: 'line',
      stack: 'Total',
      data: data['yuanshi']
    },
    {
      name: '预测值',
      type: 'line',
      stack: 'Total',
      data: data['yuce']
    },
    
  ]
};

option && myChart.setOption(option);
}

 
</script>
 
<style lang="scss" scoped>
@mixin borderColor($color: #2260FF) {
    border: 1px dashed $color;
}
 
.drag {
    position: relative;
    height: 160px;
    width: 600px;
    @include borderColor(#DEDEDE);
    border-radius: 4px;
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: center;
    margin-top: 100px;
    margin-left: 350px;

    &:active {
        @include borderColor
    }
 
    &:hover {
        @include borderColor
    }
 
    &-active {
        @include borderColor
    }
 
    &-title {
        font-size: 14px;
    }
 
    &-subtile {
        width: 450px;
        font-size: 12px;
        color: #999999;
        margin-top: 0;
        text-align: center;
    }
}
 
.file-ipt {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}
 
.filePaste-ipt {
    position: fixed;
    right: -100vw;
    opacity: 0;
}

.info-box {
    position: absolute;
    left: 57%;
    transform: translateX(-50%);
    width: 600px;
    margin-top: 60px;
    
}

.info-box p {
    font-size: 14px;
    width: 600px;
    color: #666666;
    text-indent: 2em;
}

.yanse {
    color:red !important;
    text-align: center;
}

</style>