<template>
  <div>
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      :ellipsis="false"
      @select="handleSelect"
    >
      <!-- <el-menu-item index="0">
        <img
          style="width: 100px"
          src="frontend/src/assets/logo.svg"
          alt="WV logo"
        />
      </el-menu-item> -->
      <div class="flex-grow" />

      <el-menu-item index="1">数据下载</el-menu-item>
      <el-menu-item index="2">下载记录</el-menu-item>
    </el-menu>
  </div>
  
  <div class="formDiv" v-if="activeIndex==1">
    <h2 >天气数据下载</h2>
    <el-form
      ref="ruleFormRef"
      style="max-width: 600px;display: flex;flex-direction: column;gap: 20px;"
      :model="ruleForm"
      :rules="rules"
      label-width="auto"
      class="demo-ruleForm"
      :size="formSize"
      status-icon
    >
      <el-form-item label="文件名称" prop="name">
        <el-input v-model="ruleForm.name" />
      </el-form-item>
      <el-form-item label="日期范围" required>
        <el-col :span="11">
          <el-form-item prop="date1">
            <el-date-picker
              v-model="ruleForm.date1"
              format="YYYYMMDD"
              value-format="YYYYMMDD"
              type="date"
              aria-label="起始日期"
              placeholder="起始日期"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col class="text-center" :span="2">
          <span class="text-gray-500">-</span>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="date2">
            <el-date-picker
              v-model="ruleForm.date2"
              format="YYYYMMDD"
              value-format="YYYYMMDD"
              type="date"
              aria-label="结束日期"
              placeholder="结束日期"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-form-item>

      <el-form-item label="备注" prop="desc">
        <el-input v-model="ruleForm.desc" type="textarea" />
      </el-form-item>
      <el-form-item style="">
        <div style="width:100%;display:flex;justify-content: center;">
            <el-button type="primary" @click="submitForm(ruleFormRef)">
          下载
        </el-button>
            <el-button @click="resetForm()">重置</el-button>
        </div>
        
      </el-form-item>
    </el-form>
                <div
                        style="text-align: center; transform: scale(0.8); bottom: 50px; position: fixed; width: 500px;font-size:20px">
                        <router-link class="link-fx fw-bold" to="#">
                            <span style="margin-right:10px">天气数据由</span>
                            <i class="fas fa-cloud"></i>
                            <span class="fs-4 text-body-color">Weather Vista</span>
                            <span style="margin-left:10px">提供下载</span>
                        </router-link>
                    </div>
  </div>
  <div class="tableDiv" v-if="activeIndex==2">
    <el-table :data="tableData" style="width: 100%">
      <el-table-column type="index" label="编号" width="100" />
    <el-table-column prop="zip_name" label="文件名称"  />
    <el-table-column prop="start_date" label="起始时间"  />
    <el-table-column prop="end_date" label="终止时间"  />
    <el-table-column prop="note" label="备注"  />
    <el-table-column  label="操作">
      <template #default="scope">
        <el-button type="text" size="medium" @click="del(scope.$index)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
  <div
                        style="text-align: center; transform: scale(0.8); bottom: 50px; position: fixed; width: 500px;font-size:20px">
                        <router-link class="link-fx fw-bold" to="#">
                            <span style="margin-right:10px">天气数据由</span>
                            <i class="fas fa-cloud"></i>
                            <span class="fs-4 text-body-color">Weather Vista</span>
                            <span style="margin-left:10px">提供下载</span>
                        </router-link>
                    </div>
  </div>

</template>

// <script lang="ts" setup>
import {
  ElForm,
  ElFormItem,
  ElInput,
  ElButton,
  ElMenu,
  ElMenuItem,
} from "element-plus";
import { reactive, ref, getCurrentInstance } from "vue";
import type { ComponentSize, FormInstance, FormRules } from "element-plus";
import axios from "axios";
import { ru } from "element-plus/es/locale";

const that = getCurrentInstance().appContext.config.globalProperties;
const serverUrl = that.$serverUrl;
const activeIndex = ref("1");


interface RuleForm {
  name: string;
  region: string;
  count: string;
  date1: string;
  date2: string;
  delivery: boolean;
  location: string;
  type: string[];
  resource: string;
  desc: string;
}

const formSize = ref<ComponentSize>("default");
const ruleFormRef = ref<FormInstance>();
const ruleForm = reactive<RuleForm>({
  name: "",
  region: "",
  count: "",
  date1: "",
  date2: "",
  delivery: false,
  location: "",
  type: [],
  resource: "",
  desc: "",
});

const locationOptions = ["Home", "Company", "School"];

const rules = reactive<FormRules<RuleForm>>({
  name: [{ required: true, message: "请输入文件名字", trigger: "blur" }],

  date1: [
    {
      required: true,
      message: "请填入日期",
      trigger: "change",
    },
  ],
  date2: [
    {
      required: true,
      message: "请填入日期",
      trigger: "change",
    },
  ],
});
const handleSelect = (key: string, keyPath: string[]) => {
  activeIndex.value=key
  if(key==2){
    getLogs()
  }else if(key==1){
    resetForm()
  }
  console.log(key, keyPath);
};
const submitForm = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      const formData = new FormData();
      formData.append("zip_name", ruleForm.name);
      formData.append("start_date", ruleForm.date1);
      formData.append("end_date", ruleForm.date2);
      formData.append("note", ruleForm.desc);
      fetch(serverUrl + "/api/download", {
        method: "POST",
        body: formData,
      })
        .then((res) => res.blob()) // 将响应转换为Blob
        .then((blob) => {
          // 创建一个URL来引用Blob
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.style.display = "none";
          a.href = url;
          a.download = ruleForm.name+".zip"; // 下载文件的名称
          document.body.appendChild(a);
          a.click(); // 自动点击链接进行下载
          window.URL.revokeObjectURL(url); // 释放URL
        })
        .catch((error) => console.error("Error:", error));

      console.log("submit!");
    } else {
      console.log("error submit!", fields);
    }
  });
};

const resetForm = ()=>{
  ruleForm.name=""
  ruleForm.date1=""
  ruleForm.date2=""
  ruleForm.desc=""
}


const options = Array.from({ length: 10000 }).map((_, idx) => ({
  value: `${idx + 1}`,
  label: `${idx + 1}`,
}));
const tableData=ref()
const getLogs=()=>{
  fetch(serverUrl + "/api/logs", {
        method: "GET",
      }).then(res=>res.json())
      .then(res=>{
        console.log(res);
        tableData.value=res
      })
}
const del=(row)=>{
  console.log(row);
  fetch(serverUrl + "/api/delete_log?line_number="+(row+1), {
        method: "DELETE",
      }).then(res=>res.json())
      .then(res=>{
        getLogs()
      })
}
</script>

<style scoped>
.flex-grow {
  flex-grow: 1;
}
.formDiv {
  display: flex;
  flex-direction:column;
  justify-content: flex-start;
  gap:50px;
  align-items: center;
  box-sizing: border-box;
  padding: 30px;
  background-color: #fff;
  height: calc(100% - 60px)
}

.tableDiv {
  display: flex;
  justify-content: center;
  box-sizing: border-box;
  padding: 30px;
  background-color: #fff;
  height: calc(100% - 60px)
}
</style>

