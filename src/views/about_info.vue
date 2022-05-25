<template>
  <pageHeader :title="title"></pageHeader>
  <main id="main">
    <div class="info-box">
      <el-card class="info-card custom-card">
        <!--        <h4>Update Github template</h4>-->
        <p>&nbsp;&nbsp;&nbsp;&nbsp;该软件由个人开发，开发目的是因为觉得每次下载壁纸再手动去换太麻烦了，所以动手写了这个程序。
          该软件所有数据均来自网站（wallhaven.cc）的 api 提供，如果由侵权，请联系开发者删除。
          <br/><br/>
          github：https://github.com/leoFitz1024/wallhaven</p>
      </el-card>
    </div>
    <div class="version-box">
      <el-timeline>
        <el-timeline-item v-for="(versionItem, i) in versions" class="custom-item"
                          :timestamp="versionItem.releaseTime" placement="top">
          <el-card class="custom-card">
            <h3 class="custom-card-title">Version {{ versionItem.version }}</h3>
            <ul class="fun-list">
              <li v-for="(noteItem, x) in versionItem.notes">{{ noteItem }}</li>
            </ul>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
  </main>
</template>

<script>
import {ElTimeline, ElCard, ElTimelineItem} from 'element-plus'
import pageHeader from "../components/page-header.vue";

export default {
  name: "setting",
  data() {
    return {
      title: "关于",
      versions: [
        {
          "version": "1.0.0",
          "releaseTime": "2021-12-31",
          "notes": [
            "条件筛选壁纸",
            "自动下载壁纸",
            "定时切换壁纸"
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
          "version": "3.0.0",
          "releaseTime": "2022-05-15",
          "notes": [
            "功能同Version 2.0.0",
            "更新后台实现框架为Electron"
          ]
        },
        {
          "version": "3.0.1",
          "releaseTime": "2022-05-24",
          "notes": [
            "本地图片列表增加按下载时间排序。",
            "修复图片保存路径中包含中文，导致切换壁纸黑屏的问题。",
            "增加自定义定时切换时间。"
          ]
        },
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
  },
  unmounted() {
  },
  methods: {},
  watch: {}
}

</script>

<style>
#main {
  padding: 40px 10px 10px 10px;
}

.fun-list {
  margin-top: 10px;
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
  background-color: #3c3a3a80;
  border: none;
  color: #fff;
}

.custom-card-title {
  font-size: 18px;
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
  padding: 0px;
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
