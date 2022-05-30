<template>
  <div class="bg-container" :class="$route.path === '/online' ? 'online-bg' : $route.path === '/switch'? 'switch-bg' :
$route.path === '/download' ? 'download-bg' : $route.path === '/setting'? 'setting-bg' : $route.path ==='/about'? 'about-bg' : ''"></div>
  <div class="left-menu">
    <div class="logo-wrap"></div>
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
</template>

<script>

import { start } from "./statics/js/ipcRenderer"
import { downloadFile } from "./statics/js/download"
import { getTime } from "./statics/js/date"
import { updateDownloadState} from "./statics/js/download"
import { getLocalStorage} from "./statics/js/utils"

export default {
  name: 'App',
  data() {
    return {
      clientWidth: 700,
      desktopInfo: "",
      downloadList: [],
      downloadFinishedList: []
    }
  },
  created() {
    this.loadDownloadFinishedList()
    this.loadDownloadList()
    updateDownloadState(this.updateDownloadState)
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
    // 更新状态
    updateDownloadState(data) {
      this.$nextTick(() => {
        let { id, done, progress, state} = data;
        let index = this.downloadList.findIndex(item => item.id === id)
        if (done) {
          if (progress === 100) {
            let { id, path, resolution, size, small, url } = data
            this.downloadFinishedList.splice(0, 0, { id, path, resolution, size, small, url, time: getTime() })
            if (index > -1) this.downloadList.splice(index, 1)
          }else if(state === "cancelled"){
            if (index > -1) this.downloadList.splice(index, 1)
          }
          localStorage.setItem("downloadList",JSON.stringify(this.downloadList))
          localStorage.setItem("downloadFinishedList",JSON.stringify(this.downloadFinishedList))
        } else {
          if (index > -1) {
            this.downloadList.splice(index,1, data);
          }else{
            this.downloadList.splice(0,1, data);
          }
          localStorage.setItem("downloadList",JSON.stringify(this.downloadList))
        }
      })
    },
    loadDownloadFinishedList() {
      let downloadFinishedListStr = getLocalStorage("downloadFinishedList","[]","String")
      if (downloadFinishedListStr != null) {
        this.downloadFinishedList = JSON.parse(downloadFinishedListStr)
        if (this.downloadFinishedList.length > 20) {
          this.downloadFinishedList.splice(19,this.downloadFinishedList.length - 20)
          localStorage.setItem("downloadFinishedList", JSON.stringify(this.downloadFinishedList))
        }

      }
    },
    loadDownloadList(){
      let downloadListStr = getLocalStorage("downloadList","[]","String")
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
        'api_params': getLocalStorage("api_params", "categories=111&purity=100&sorting=hot&order=desc", "String"),
        'api_key': getLocalStorage("api_key", "", "String"),
        'schedule_time': getLocalStorage("schedule_time", 0, "Number"),
        'custom_schedule_time': getLocalStorage("custom_schedule_time", 5, "Number"),
        'download_dir': getLocalStorage("download_dir", "", "String"),
        'current_page': getLocalStorage("current_page", 1, "Number"),
        'page_index': getLocalStorage("page_index", 0, "Number"),
        'local_bg_index': getLocalStorage("local_bg_index", 0, "Number"),
        'total_page': getLocalStorage("total_page", 0, "Number"),
        'switch_model': getLocalStorage("switch_model", "online", "String"),
        'auto_start': getLocalStorage("auto_start", 0, "Number"),
        'full_model': getLocalStorage("full_model", 1, "Number"),
        'bg_color': getLocalStorage("bg_color", "rgb(8,8,8)", "String"),
      }
      start(JSON.stringify(localStorageMap), this)
    }
  },
  components: {},
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
  top: 0;
  left: 0;
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

.logo-wrap {
  width: 100%;
  height: 150px;
  background: url("./statics/icons/logo.png") no-repeat;
  background-size: 90%;
  background-position: 40% 20%;

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
