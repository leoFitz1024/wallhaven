<template>
  <pageHeader :title="title"></pageHeader>
  <main id="main">
    <div class="setting-list">
      <div class="setting-group">
        <div class="setting-group-title">系统设置</div>
        <div class="setting-group-content">
          <div class="setting-item">
            <a class="setting-title">开机自启</a>
            <div class="setting-content">
              <el-radio class="custom-radio" v-model="autoStart" :label="0" size="large">关闭&#12288;&#12288;</el-radio>
              <el-radio class="custom-radio" v-model="autoStart" :label="1" size="large">打开</el-radio>
            </div>
          </div>
          <div class="setting-item">
            <a class="setting-title">网络代理</a>
            <el-tooltip placement="top" effect="light" popper-class="custom-tips api-key-tooltip">
              <template #content>设置http代理，解决网络问题。</template>
              <a class="api-key-tips"><i class="fas fa-question-circle"></i></a>
            </el-tooltip>
            <el-switch
                v-model="proxy.enable"
                inline-prompt
                active-text="开"
                inactive-text="关"
                @click="closeProxy()"
                style="--el-switch-off-color: #ff4949; margin-left: 10px"
            />
            <div class="setting-content">
              <el-select
                  v-model="proxy.protocol"
                  placeholder="协议"
                  style="width: 90px"
              ><el-option
                    v-for="item in protocols"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                />
              </el-select>
              <span style="margin-left: 4%">地址:</span>
              <el-input class="proxy-input" v-model="proxy.address"/>
              <span style="margin-left: 4%">端口:</span>
              <el-input class="proxy-port-input" v-model="proxy.port"/>
            </div>
          </div>
          <div class="setting-item">
            <a class="setting-title">API Key</a>
            <el-tooltip placement="top" effect="light" popper-class="custom-tips api-key-tooltip">
              <template #content>设置API Key可解锁NSFW图片<br/>访问：“https://wallhaven.cc/settings/account” 获取API Key
              </template>
              <a class="api-key-tips"><i class="fas fa-question-circle"></i></a>
            </el-tooltip>
            <div class="setting-content">
              <el-input class="api-key-input" v-model="apiKey"/>
            </div>
          </div>
          <div class="setting-item">
            <a class="setting-title">壁纸文件夹</a>
            <div class="setting-content">
              <el-input class="images-folder" readonly="true" v-model="imagesFolder"/>
              <button type="button" id="select-folder" @click="selectFolder">选择</button>
              <button type="button" id="open-folder" @click="openFolder"><i class="fas fa-folder-open"></i></button>
            </div>
          </div>
        </div>
        <div class="setting-group-title">壁纸设置</div>
        <div class="setting-group-content">
          <div class="setting-item">
            <a class="setting-title">切换模式</a>
            <div class="setting-content">
              <el-radio class="custom-radio" v-model="switchModel" label="online" size="large">在线切换</el-radio>
              <el-radio class="custom-radio" v-model="switchModel" label="local" size="large">本地切换</el-radio>
            </div>
          </div>
          <div class="setting-item">
            <a class="setting-title">填充模式</a>
            <div class="setting-content">
              <el-radio v-model="fullModel" :label="0" size="large">填充</el-radio>
              <el-radio v-model="fullModel" :label="1" size="large">适应</el-radio>
              <el-radio v-model="fullModel" :label="2" size="large">拉伸</el-radio>
              <el-radio v-model="fullModel" :label="3" size="large">平铺</el-radio>
              <el-radio v-model="fullModel" :label="4" size="large">居中</el-radio>
              <el-radio v-model="fullModel" :label="5" size="large">跨区</el-radio>
              <div class="model-preview-title">
                <a>预览</a>
              </div>
              <div class="model-preview">
                <div class="bg-color" :style="{backgroundColor:bgColor}">
                  <div class="bg-view" :class="fullModel === 0 ? 'bg-fill'
                  : fullModel === 1 ? 'bg-adapt' : fullModel === 2 ? 'bg-stretch'
                  : fullModel === 3 ? 'bg-tile': fullModel === 4 ? 'bg-center'
                  : fullModel === 5 ? 'bg-trans-region' : ''"></div>
                </div>
                <div class="bg-color-selector">背景颜色：
                  <el-color-picker color-format="rgb" v-model="bgColor"/>
                </div>
              </div>
            </div>
          </div>
          <div class="setting-item">
            <a class="setting-title">定时切换</a>
            <div class="setting-content">
              <el-radio v-model="scheduleTime" :label="0" size="large">关闭</el-radio>
              <el-radio v-model="scheduleTime" :label="10" size="large">10分钟</el-radio>
              <el-radio v-model="scheduleTime" :label="30" size="large">30分钟</el-radio>
              <el-radio v-model="scheduleTime" :label="60" size="large">1小时</el-radio>
              <el-radio v-model="scheduleTime" :label="180" size="large">3小时</el-radio>
              <el-radio v-model="scheduleTime" :label="-1" size="large">自定义：
                <el-input-number class="customer-schedule" :min="5" :max="1440" v-model="customScheduleTime">
                </el-input-number>
                分钟
              </el-radio>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="setting-bottom">
      <button type="button" class="clear-submit"
              title="重置所有配置数据，并重启应用。" @click="clearData">
        重置应用
      </button>
      <button type="button" :disabled="saving" class="config-submit" :class="saving ? 'saving' : ''"
              @click="saveConfig">
        保存设置
        <span v-show="saving" class="fa-spinner-span"><i class="fas fa-spinner"></i></span></button>
    </div>
  </main>
</template>

<script>
import {ElRadio, ElInput, ElInputNumber, ElTooltip, ElColorPicker, ElSwitch, ElSelect, ElOption} from 'element-plus'
import pageHeader from "../components/page-header.vue";
import {updateConfig, showOpenDialogSync, openFolder, clearData, sendCloseProxy} from "../statics/js/ipcRenderer"
import {getLocalStorage} from "../statics/js/utils";

const hostRegx = /^(www\.)?(([0-9]{1,3}\.){3}[0-9]{1,3}|([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,6})(:[0-9]{1,4})?$/
const portRegx = /^([0-9]{1,5})?$/


export default {
  name: "setting",
  data() {
    return {
      title: "设置",
      saving: false,
      switchModel: "online",
      imagesFolder: "",
      scheduleTime: 0,
      customScheduleTime: 5,
      autoStart: 0,
      apiKey: "",
      protocols: [
        {
          value: 'http',
          label: 'http',
        },{
          value: 'socks',
          label: 'socks',
        }
        // ,{
        //   value: 'custom',
        //   label: '自定义',
        // }
      ],
      proxy: {
        "enable": false,
        "protocol": "http",
        "address": "",
        "port": ""
      },
      fullModel: 0,
      bgColor: "rgb(88,88,88)"
    }
  },
  components: {
    ElRadio,
    ElInput,
    ElInputNumber,
    ElTooltip,
    ElColorPicker,
    ElSwitch,
    ElSelect,
    ElOption,
    pageHeader
  },
  props: [],
  created() {
    this.imagesFolder = getLocalStorage("downloadDir", "", "String")
    this.switchModel = getLocalStorage("switchModel", "online", "String")
    this.fullModel = getLocalStorage("fullModel", 1, "Number")
    this.bgColor = getLocalStorage("bgColor", "rgb(8,8,8)", "String")
    this.scheduleTime = getLocalStorage("scheduleTime", 0, "Number")
    this.apiKey = getLocalStorage("apiKey", "", "String")
    this.autoStart = getLocalStorage("autoStart", 0, "Number")
    this.proxy = getLocalStorage("proxy", {"address": "", "port": ""}, "Object")
  },
  mounted() {
  },
  unmounted() {
  },
  methods: {
    selectFolder() {
      showOpenDialogSync(localStorage.getItem("downloadDir")).then(res => {
        this.imagesFolder = res
      })
    },
    openFolder() {
      openFolder(this.imagesFolder).then(res => {
        if (!res.success) {
          this.$message({
            message: res.msg,
            type: res.type,
            duration: res.type === "success" ? 1200 : 2000,
            customClass: 'customer-message'
          })
        }
      })
    },
    //检查配置格式
    async checkConfig() {
      return this.checkProxy() && await this.checkApiKey()
    },
    //关闭网络代理
    closeProxy(){
      if(this.proxy.enable !== true){
        sendCloseProxy()
      }
    },
    checkProxy() {
      if (this.proxy.address !== "" && !hostRegx.test(this.proxy.address)) {
        this.$message({
          message: "代理地址不合法",
          type: "error",
          duration: 2000,
          customClass: 'customer-message'
        })
        return false;
      }
      if (this.proxy.port !== "" && !portRegx.test(this.proxy.port)) {
        this.$message({
          message: "代理端口不合法",
          type: "error",
          duration: 2000,
          customClass: 'customer-message'
        })
        return false;
      }
      if (this.proxy.enable && (this.proxy.address === "" || this.proxy.port === "")){
        this.proxy.enable = false
      }
      return true
    },
    async checkApiKey() {
      let success = true
      if (this.apiKey !== "") {
        await this.$wallhavenApi.search(`/search?apikey=${this.apiKey}`).then(res => {
          if (res === "Unauthorized") {
            this.$message({
              message: "ApiKey不正确，已重置",
              type: "error",
              duration: 2000,
              customClass: 'customer-message'
            })
            this.apiKey = ""
            success = false
          }
        }).catch(err => {
          this.$message({
            message: "检查ApiKey失败：" + err,
            type: "error",
            duration: 2000,
            customClass: 'customer-message'
          })
          this.apiKey = ""
          success = false
        })
      }
      return success
    },
    async saveConfig() {
      this.saving = true
      if (!await this.checkConfig()) {
        this.saving = false
        return
      }
      let params = {
        scheduleTime: this.scheduleTime,
        customScheduleTime: this.customScheduleTime,
        downloadDir: this.imagesFolder,
        switchModel: this.switchModel,
        fullModel: this.fullModel,
        bgColor: this.bgColor,
        autoStart: this.autoStart,
        proxy: this.proxy
      }
      updateConfig(params).then(res => {
        this.$message({
          message: res.msg,
          type: res.type,
          duration: res.type === "success" ? 1200 : 2000,
          customClass: 'customer-message'
        })
        if (res.success) {
          localStorage.setItem("apiKey", this.apiKey)
          localStorage.setItem("scheduleTime", params['scheduleTime'])
          localStorage.setItem("customScheduleTime", params['customScheduleTime'])
          localStorage.setItem("downloadDir", params['downloadDir'])
          localStorage.setItem("switchModel", params['switchModel'])
          localStorage.setItem("fullModel", params['fullModel'])
          localStorage.setItem("bgColor", params['bgColor'])
          localStorage.setItem("autoStart", params['autoStart'])
          localStorage.setItem("proxy", JSON.stringify(params['proxy']))
        }
      }).finally(res => {
        this.saving = false
      })
    },
    clearData() {
      clearData();
    }
  },
  watch: {}

}
</script>

<style scoped>
@import url("../statics/css/list.css");

#main {
  padding-top: 40px;
  text-align: center;
}

.config-submit span {
  margin-left: 3px;
  text-align: center;
  cursor: pointer;
  color: #ddd;
  text-shadow: -1px -1px 0 #000;
  border-radius: 3px;
}

.fa-spinner {
  animation: spin 0.8s infinite linear;
}


.model-preview-title {
  margin: 8px 0px;
}

.bg-color-selector {
  width: 454px;
  text-align: center;
  padding: 10px 0px;
}

.bg-color {
  width: 454px;
  height: 229px;
  border-radius: 3px;
  border: 2px solid #d3dce6;
}

.bg-view {
  margin: 0px 0px 0px 0px;
  padding: 0;
  width: 450px;
  height: 225px;
  background-color: #00ccdd;
  background: url("../statics/img/preview-bg.png");

}

/*填充*/
.bg-view.bg-fill {
  background-size: cover;
  background-position: 0% 31.5%;
}

/*适应*/
.bg-view.bg-adapt {
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center center;
}

/*拉伸*/
.bg-view.bg-stretch {
  background-size: 100% 100%;
}

/*平铺*/
.bg-view.bg-tile {
  background-repeat: repeat-x;
}

.bg-view.bg-center {
  background-repeat: no-repeat;
  background-position: 50%;
}

.bg-view.bg-trans-region {
  background-size: cover;
  background-position: 50%;
}

.setting-bottom {
  text-align: center;
}

.api-key-tips {
  margin: 0.5em 0.25em;
  /*padding: 0.5em 1em;*/
}

.setting-list {
  margin: 20px auto;
  width: 50%;
  text-align: left;
}

.setting-item {
  margin-bottom: 10px;
}

.setting-group {
  margin-bottom: 10px;
}

.setting-group-content {
  padding: 10px 10px 10px 20px;
}

.setting-group-title {
  font-size: 18px;
  text-align: center;
}

.setting-title {
  display: inline-block;
  font-size: 16px;
}

.setting-content {
  font-size: 15px;
  padding: 5px 5px 5px 20px;
}


#open-folder, #select-folder {
  display: inline-block;
  display: inline-block;
  margin: 0.5em 0.25em;
  padding: 0.5em 1em;
  text-align: center;
  cursor: pointer;
  color: #ddd;
  text-shadow: -1px -1px 0 #000;
  border-radius: 3px;
  background-color: #204650;
  background-image: linear-gradient(to bottom, #85bbc7 0, #183640 100%);
  background-size: 100% 150%;
  background-position: 0 100%;
  transition-property: color, background, text-shadow, box-shadow, border-color;
  transition-duration: .25s;
}

#open-folder {
  display: inline-block;
  background-image: linear-gradient(to bottom, #275660 0, #183640 100%);
}

.config-submit, .clear-submit {
  display: inline-block;
  margin: 0.5em 0.25em;
  padding: 0.5em 1em;
  text-align: center;
  cursor: pointer;
  text-shadow: -1px -1px 0 #000;
  border-radius: 3px;
  color: #fff;
  background-color: #2e86de;
  background-image: linear-gradient(to bottom, #00d2d3 0, #01a3a4 100%);
  background-size: 100% 150%;
  background-position: 0 100%;
  transition-property: color, background, text-shadow, box-shadow, border-color;
  transition-duration: .25s;
}

.clear-submit {
  color: #ddd;
  background-color: #204650;
  background-image: linear-gradient(to bottom, #275660 0, #183640 100%);
}

#select-folder:hover, .clear-submit:hover, .config-submit:hover, #open-folder:hover {
  background-position: 0 0;
}
</style>

<style>

.setting-group span {
  color: #dddddd !important;
}

.custom-radio {
  margin-right: 180px;
}

.customer-schedule {
  width: 130px;
}

.images-folder {
  display: inline-block;
  width: 70%;
}

.api-key-input {
  display: inline-block;
  width: 70%;
}

.proxy-input {
  display: inline-block;
  width: 30%;
}

.proxy-port-input {
  display: inline-block;
  width: 80px;
}

.api-key-tips {
  user-select: text;
  text-align: center;
  line-height: 18px;
}
</style>
