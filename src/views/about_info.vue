<template>
  <pageHeader :title="title"></pageHeader>
  <main id="main">
    <div class="info-box">
      <el-card class="info-card custom-card">
        <p>&nbsp;&nbsp;&nbsp;&nbsp;该软件开源免费，由个人开发，开发目的是因为觉得每次下载壁纸再手动去换太麻烦了，所以动手写了这个程序。
          该软件所有数据均来自网站（wallhaven.cc）的 api 提供，如有侵权，请联系开发者删除。
        </p>
        <br>
        <p>开源地址：
          <span class="project-link" data-herf="https://github.com/leoFitz1024/wallhaven"
                @click="openLink">Wallhaven</span>
        </p>
      </el-card>
      <el-card class="info-card custom-card qr-card">
        <h3>Good Job! 如果您觉得该软件不错，可以给作者一点小小的鼓励。</h3>
        <div style="line-height: 40px">所有赞赏者将会永久展示在赞赏名单中，为了保证您的昵称出现在在致谢名单上，赞赏时请备注上您的昵称。</div>
        <div class="qr-code-content">
          <div class="qr-card-item">
            <img class="qrcode" src="../statics/img/afd.png" alt="">
            <h3>爱发电</h3>
          </div>
          <div class="qr-card-item">
            <img class="qrcode" src="../statics/img/qr.jpg" alt="">
            <h3>赞赏二维码</h3>
          </div>
          <div class="qr-card-item">
            <img class="qrcode" src="../statics/img/qq.png" alt="">
            <h3>问题反馈qq群</h3>
          </div>
        </div>
      </el-card>
      <el-card class="info-card custom-card qr-card">
        <h3 style="font-size: larger">致谢名单</h3>
        <div class="user-center">
          <div class="user-item item-center" v-for="user in acknowledgementList">
              <img :src="user.avatar !== undefined && user.avatar !== '' ? user.avatar :  defaultAvatar"
                   class="rounded-full user-avatar"
                   loading="lazy">
              {{user.name}}
          </div>
        </div>
      </el-card>
      <el-card class="update-log-card">
        <h3 style="text-align: center; font-size: larger">更新日志</h3>
        <div class="version-box">
          <el-timeline>
            <el-timeline-item v-for="(versionItem, i) in versions" class="custom-item"
                              :timestamp="versionItem.releaseTime" placement="top">
              <el-card class="update-log-item-card">
                <h3 class="custom-card-title">Version {{ versionItem.version }}</h3>
                <ul class="fun-list">
                  <li v-for="(noteItem, x) in versionItem.notes">{{ noteItem }}</li>
                </ul>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-card>
    </div>
  </main>
</template>

<script>
import {ElTimeline, ElCard, ElTimelineItem} from 'element-plus'
import {openLink} from '../statics/js/ipcRenderer';
import pageHeader from "../components/page-header.vue";
import axios from "axios";

export default {
  name: "setting",
  data() {
    return {
      title: "关于",
      defaultAvatar: "https://pic1.afdiancdn.com/default/avatar/avatar-orange.png?imageView2/1/w/120/h/120",
      acknowledgementList: [],
      versions: [
        {
          "version": "3.1.0",
          "releaseTime": "2023-07-17",
          "notes": [
            "代理功能支持http协议/socks协议",
            "支持自动更新"
          ]
        },
        {
          "version": "3.0.3",
          "releaseTime": "2023-05-21",
          "notes": [
            "增加设置网络代理功能。"
          ]
        },
        {
          "version": "3.0.2",
          "releaseTime": "2022-07-19",
          "notes": [
            "增加关键词搜索功能。",
            "修复下载任务列表显示问题。"
          ]
        },
        {
          "version": "3.0.1",
          "releaseTime": "2022-05-24",
          "notes": [
            "本地图片列表增加按下载时间排序。",
            "本地图片列表增加删除按钮。",
            "修复图片保存路径中包含中文，导致切换壁纸黑屏的问题。",
            "增加自定义定时切换时间。"
          ]
        },
        {
          "version": "3.0.0",
          "releaseTime": "2022-05-15",
          "notes": [
            "功能同Version 2.0.0",
            "更新后台实现框架为Electron"
          ]
        },
        {
          "version": "2.0.0",
          "releaseTime": "2022-01-24",
          "notes": [
            "条件筛选壁纸",
            "在线查看壁纸",
            "一键设置壁纸",
            "下载任务列表",
            "在线定时切换壁纸",
            "本地文件夹切换壁纸",
            "多种壁纸自适应模式",
            "开机自启"
          ]
        },
        {
          "version": "1.0.0",
          "releaseTime": "2021-12-31",
          "notes": [
            "条件筛选壁纸",
            "自动下载壁纸",
            "定时切换壁纸"
          ]
        }
      ]
    }
  },
  components: {
    ElTimeline,
    ElCard,
    ElTimelineItem,
    pageHeader
  },
  props: [],
  created() {

  },
  mounted() {
    axios.get('https://tmqt-sh-1257108036.cos-website.ap-shanghai.myqcloud.com/wallhaven/online.json')
        .then(response => {
          this.acknowledgementList = response.data.acknowledgement
          this.defaultAvatar = response.data.defaultAvatar
        })
        .catch(error => {
          console.error("获取致谢名单失败：" + error)
          this.acknowledgementList = [
            {
              "avatar": "https://avatars.githubusercontent.com/u/6481596?v=4&amp;size=64",
              "name": "浮生梦"
            },
            {
              "name": "爱发电用户_RasX"
            },
            {
              "name": "wjk3719"
            },
            {
              "name": "arijoes"
            }
          ]
        })
  },
  unmounted() {
  },
  methods: {
    openLink(event) {
      openLink(event.target.dataset.herf)
    }
  },
  watch: {}
}

</script>

<style>
#main {
  padding: 40px 10px 10px 10px;
}

.project-link:hover {
  color: #60f5d2;
}

.qr-card {
  margin-top: 20px;
  text-align: center;
}

.qr-code-content {
  margin-top: 20px;
  text-align: center;
}

.qr-card-item {
  display: inline-block;
  text-align: center;
  margin: 0 10px 0 20px;
}

.qrcode {
  width: 120px;
  height: 120px;
}

.user-center {
  padding: 20px 30px;
  line-height: 1.4;
  font-size: 16px;
  font-weight: 400;
}

.item-center {
  display: inline-flex;
  align-items: center;
  margin: 0 10px;
}


.rounded-full {
  border-radius: 9999px;
  width: 2rem;
  height: 2rem;
}

.user-avatar {
  margin-right: 3px;
}

.fun-list li {
  font-size: 16px;
  margin-left: 20px;
  list-style-type: disc;
  line-height: 25px !important;
}

.custom-item div {
  color: #fff !important;
}

.custom-card {
  background-color: rgba(175, 174, 174, 0.5);
  border: none;
  color: #fff;
}

.update-log-card{
  background-color: rgba(175, 174, 174, 0.5);
  font-size: 16px;
  border: none;
  color: #fff;
  margin-top: 20px;
}

.update-log-item-card{
  border: none;
  background-color: #2d4060c7;
}

.custom-card h3 {
  padding: 0px !important;
  margin: 0px !important;
}

.custom-card > div {
  padding: 10px !important;
}

.info-box {
  margin-top: 30px;
  padding: 10px 80px;

}

.info-card {
  padding-top: 5px;
  font-size: 16px;
  user-select: text;
}

.info-card p {
  line-height: 25px !important;
  user-select: text;
}

.version-box {
  margin-top: 20px;
  padding: 0 80px;
}
</style>
