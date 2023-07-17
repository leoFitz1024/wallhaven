<template>
  <div class="bg-container" :class="$route.path === '/online' ? 'online-bg' : $route.path === '/switch'? 'switch-bg' :
$route.path === '/download' ? 'download-bg' : $route.path === '/setting'? 'setting-bg' : $route.path ==='/about'? 'about-bg' : ''"></div>
  <div class="left-menu">
    <img class="logo-wrap" src="./statics/icons/logo.png"/>
    <div class="version-wrap">v{{ version }}</div>
    <div class="menu-wrap">
      <label class="menu-title">我的壁纸</label>
      <ul class="menu-ul">
        <li class="menu-item">
          <router-link to="/online" class="menu-native">
            <i class="fas fa-cloud"></i>
            在线壁纸<span class="li-border"/>
          </router-link>
        </li>
        <li class="menu-item">
          <router-link to="/switch" class="menu-native">
            <i class="fas fa-folder"></i>
            本地列表<span class="li-border"/>
          </router-link>
        </li>
        <li class="menu-item">
          <router-link to="download" class="menu-native">
            <i class="fas fa-inbox-in"></i>
            下载中心<span class="li-border"/>
          </router-link>
        </li>
      </ul>
      <label class="menu-title more">更多</label>
      <ul class="menu-ul">
        <li class="menu-item">
          <router-link to="setting" class="menu-native">
            <i class="fas fa-cog"></i>
            设置<span class="li-border"/>
          </router-link>
        </li>
        <li class="menu-item">
          <router-link to="about" class="menu-native">
            <i class="fas fa-info-circle"></i>
            关于<span class="li-border"/>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
  <div class="container" :style="{width:calContainerW + 'px'}">
    <router-view @delDownRecorder="delDownRecorder"></router-view>
  </div>
  <el-dialog v-model="showUpdateDialog" title="版本更新" top="15%" width="25%" center>
    <div>
      <div style="margin-bottom: 5px">
      检测到新的版本{{ updateInfo.version }}，是否现在进行更新？
      </div>
        <li v-for="item in updateInfo.releaseNotes">{{ item }}</li>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="showUpdateDialog = false">暂不更新</el-button>
        <el-button type="primary" @click="downloadUpdate()">
          立即更新
        </el-button>
      </span>
    </template>
  </el-dialog>
  <div class="update-process-container" v-show="showUpdateProcessDiv">
    <div style="text-align: center; margin-bottom: 5px">
      正在下载新版本...{{ this.$formatSpeed(versionDownSpeed) }}
    </div>
    <el-progress :text-inside="true" :stroke-width="15" :percentage="versionDownPercentage" :striped="true"
                 :striped-flow="true"/>
  </div>
</template>

<script>

import {start} from "./statics/js/ipcRenderer"
import {downloadFile} from "./statics/js/download"
import {getTime} from "./statics/js/date"
import {updateDownloadState} from "./statics/js/download"
import {
  onUpdateMessage,
  onUpdateErrorMessage,
  sendDownloadUpdate,
  onDownloadProgress
} from "./statics/js/update"
import {getLocalStorage} from "./statics/js/utils"
import {ElMessage, ElMessageBox, ElProgress, ElButton, ElDialog} from 'element-plus'

export default {
  name: 'App',
  data() {
    return {
      //显示版本更新提示框
      showUpdateDialog: false,
      //新版信息
      updateInfo: {
        version: "",
        releaseNotes: []
      },
      //是否显示版本下载div
      showUpdateProcessDiv: false,
      //新版本下载进度
      versionDownPercentage: 0,
      //新版本下载速度
      versionDownSpeed: 0,
      //app版本
      version: APP_VERSION,
      clientWidth: 700,
      desktopInfo: "",
      //图片下载列表
      downloadList: [],
      //图片下载完成列表
      downloadFinishedList: []
    }
  },
  components: {
    ElProgress,
    ElMessage,
    ElMessageBox,
    ElButton,
    ElDialog
  },
  created() {
    this.loadDownloadFinishedList()
    this.loadDownloadList()
    updateDownloadState(this.updateDownloadState)
    onUpdateMessage(this.showUpdateMessage)
    onUpdateErrorMessage(this.showUpdateErrorMessage)
    onDownloadProgress(this.updateVersionDownloadProgress)
  },
  mounted() {
    this.clientWidth = document.documentElement.clientWidth;
    window.addEventListener('resize', this.onresize);
    this.startApp()
  },
  watch: {
    downloadListLen: {
      deep: true,
      handler(val) {
        this.downloadListLen.sort(function (a, b) {
          return b.time - a.time;
        })
      }
    },
    downloadFinishedList: {
      deep: true,
      handler(val) {
        this.downloadFinishedList.sort(function (a, b) {
          return b.time - a.time;
        })
      }
    }
  },
  methods: {
    onresize() {
      if (document.documentElement.clientWidth !== undefined) {
        this.clientWidth = document.documentElement.clientWidth;
      }
    },
    addDownloadFile(task) {
      return downloadFile(task)
    },
    //显示更新消息
    showUpdateMessage(info) {
      this.updateInfo = info;
      this.showUpdateDialog = true
    },
    //显示更新失败提示
    showUpdateErrorMessage(error) {
      ElMessageBox.alert('更新失败' + error, '错误', {
        confirmButtonText: '确认',
        callback: (action) => {
        },
      })
      this.showUpdateDialog = false
      this.showUpdateProcessDiv = false
    },
    downloadUpdate() {
      this.showUpdateDialog = false
      this.showUpdateProcessDiv = true
      sendDownloadUpdate()
    },
    //更新新版本下载进度
    updateVersionDownloadProgress(progress) {
      this.versionDownPercentage = progress.percentage
      this.versionDownSpeed = progress.speed
    },
    // 更新图片下载状态
    updateDownloadState(data) {
      this.$nextTick(() => {
        let {id, done, progress, state} = data;
        let index = this.downloadList.findIndex(item => item.id === id)
        if (done) {
          if (progress === 100) {
            let {id, path, resolution, size, small, url} = data
            this.downloadFinishedList.splice(0, 0, {id, path, resolution, size, small, url, time: getTime()})
            if (index > -1) this.downloadList.splice(index, 1)
          } else if (state === "cancelled") {
            if (index > -1) this.downloadList.splice(index, 1)
          }
          localStorage.setItem("downloadList", JSON.stringify(this.downloadList))
          localStorage.setItem("downloadFinishedList", JSON.stringify(this.downloadFinishedList))
        } else {
          if (index > -1) {
            this.downloadList.splice(index, 1, data);
          } else {
            this.downloadList.splice(0, 0, data);
          }
          localStorage.setItem("downloadList", JSON.stringify(this.downloadList))
        }
      })
    },
    loadDownloadFinishedList() {
      let downloadFinishedListStr = getLocalStorage("downloadFinishedList", "[]", "String")
      if (downloadFinishedListStr != null) {
        this.downloadFinishedList = JSON.parse(downloadFinishedListStr)
        if (this.downloadFinishedList.length > 20) {
          this.downloadFinishedList.splice(19, this.downloadFinishedList.length - 20)
          localStorage.setItem("downloadFinishedList", JSON.stringify(this.downloadFinishedList))
        }

      }
    },
    loadDownloadList() {
      let downloadListStr = getLocalStorage("downloadList", "[]", "String")
      if (downloadListStr != null) {
        this.downloadList = JSON.parse(downloadListStr)
        this.downloadList.forEach(item => item.state = "paused")
      }
    },
    delDownRecorder(url) {
      delete this.downloadFinishedList[url]
      localStorage.setItem("downloadFinishedList", JSON.stringify(this.downloadFinishedList))
    },
    startApp() {
      let localStorageMap = {
        apiParams: getLocalStorage("apiParams", "categories=111&purity=100&sorting=hot&order=desc", "String"),
        apiKey: getLocalStorage("apiKey", "", "String"),
        scheduleTime: getLocalStorage("scheduleTime", 0, "Number"),
        customScheduleTime: getLocalStorage("customScheduleTime", 5, "Number"),
        downloadDir: getLocalStorage("downloadDir", "", "String"),
        currentPage: getLocalStorage("currentPage", 1, "Number"),
        pageIndex: getLocalStorage("pageIndex", 0, "Number"),
        local_bg_index: getLocalStorage("local_bg_index", 0, "Number"),
        totalPage: getLocalStorage("totalPage", 0, "Number"),
        switchModel: getLocalStorage("switchModel", "online", "String"),
        autoStart: getLocalStorage("autoStart", 0, "Number"),
        proxy: getLocalStorage("proxy", {"address": "", "port": ""}, "Object"),
        fullModel: getLocalStorage("fullModel", 1, "Number"),
        bgColor: getLocalStorage("bgColor", "rgb(8,8,8)", "String"),
      }
      start(JSON.stringify(localStorageMap), this)
    }
  },
  computed: {
    calContainerW() {
      let width = this.clientWidth - 200;
      if (width < 800) {
        return 800;
      } else {
        return width;
      }
    }
  }

}
</script>

<style scoped>

a:link,
a:visited {
  /*去掉a标签链接的下划线的效果*/
  text-decoration: none;
}

.logo-wrap {
  margin: 10px 0 2px 0;
  padding: 0 8px 0 8px;
  width: 95%;
}

.version-wrap {
  text-align: center;
  margin-bottom: 30px;
}

.update-process-container {
  padding-top: 5px;
  z-index: 999;
  width: 100%;
  bottom: 0;
  position: fixed;
  background: rgba(96, 96, 96, 0.87);
  -moz-box-shadow: 0 -3px 9px #070805;
  -webkit-box-shadow: 0 -3px 9px #070805;
  box-shadow: 0 -3px 9px #070805;
}

.bg-container {
  position: fixed;
  top: 0;
  left: 0;
  min-height: 100%;
  width: 100%;
  overflow: hidden;
  background-color: #0c0e29;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: left top;
  z-index: -1;
  transition: background 0.8s;
}

.online-bg {
  background-image: url(statics/img/online-bg.jpg);
}

.switch-bg {
  background-image: url(statics/img/switch-bg.jpg);
}

.download-bg {
  background-image: url(statics/img/download-bg.jpg);
}

.setting-bg {
  background-image: url(statics/img/setting-bg.jpg);
}

.about-bg {
  background-image: url(statics/img/about-bg.jpg);
}

.bg-container:before {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: -2;
  backdrop-filter: blur(20px);
}


.left-menu a,
.left-menu label {
  font-size: 1.1rem;
}

.left-menu {
  z-index: 998;
  position: fixed;
  color: #fff;
  float: left;
  width: 180px;
  height: 100%;
  /*background-color: rgba(39, 42, 44, .75);*/
  /*background-image: linear-gradient(to right, #292c2f 0, rgba(34, 34, 34, .5) 100%);*/
  box-shadow: 0 0 0 1px #222, 5px 0px 5px rgb(0 0 0 / 50%);
}

.menu-title {
  display: block;
}

.more {
  margin-top: 100px;
}

.menu-wrap {
  text-align: left;
  padding: 0 23px;
}

.menu-ul {
  list-style-type: none;
  padding-top: 5px;
  padding-left: 25px;
}

.menu-item {
  margin-top: 20px;
  color: #c6c6c6;
}

.menu-item > i {
  margin-right: 5px;
}

.menu-native {
  display: inline-block;
  color: #c6c6c6;
  min-width: 60px;
}

.menu-native:hover {
  color: #fff;
}

.menu-native.router-link-active {
  color: #fff;
}

.li-border {
  padding: 0;
  margin: 3px 0 0 0;
  display: block;
  border-radius: 3px;
  background: transparent;
  width: 100%;
  height: 2px;
}

.menu-native:hover > .li-border {
  background: linear-gradient(to right, rgba(2, 108, 209, 255), 50%, rgba(35, 196, 214, 255));
}

.menu-native.router-link-active > .li-border {
  background: linear-gradient(to right, rgba(2, 108, 209, 255), 50%, rgba(35, 196, 214, 255));
}

.container {
  /* padding-top: 50px; */
  margin-left: 180px;
  /*float: left;*/
}

.container::-webkit-scrollbar {
  display: none;
}
</style>
