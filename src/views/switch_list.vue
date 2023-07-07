<template>
  <imgPreview @close="closePreview" :showing="showImgPre" :imgInfo="preImgInfo"></imgPreview>
  <div>
    <pageHeader :title="title"></pageHeader>
    <main id="main">
      <div id="thumbs" class="thumbs-container thumb-listing infinite-scroll">
        <section class="thumb-listing-page" v-for="(sectionItem, i) in pageData.sections">
          <header v-if="i !== 0" class="thumb-listing-page-header">
            <h2>Page <span class="thumb-listing-page-num">{{ i + 1 }}</span> / {{ pageData.totalPage }}</h2>
            <a class="icon to-top" href="#top" title="Back to top">
              <i class="far fa-lg fa-chevron-up"></i>
            </a>
          </header>
          <ul>
            <li v-for="(liItem, index) in sectionItem">
              <figure class="thumb" :class="'thumb-' + (liItem.id) + ' thumb-general'"
                      :data-wallpaper-id="liItem.id" style="width:300px;height:200px">
                <a class="thumb-btn thumb-btn-fav jsAnchor overlay-anchor" title="设为壁纸" @click="setBg(liItem)">
                  <i class="fas fa-repeat-alt"></i>
                </a>
                <img alt="loading" loading="lazy" style="width: 300px;height: 200px;object-fit:cover"
                     class="lazyload loaded" :data-src="liItem.src === undefined ? liItem.base64 : liItem.src"
                     :src="liItem.src === undefined ? liItem.base64 : liItem.src"/>
                <a class="preview" @click="preview(liItem)"></a>
                <div class="thumb-info">
                  <span class="wall-res">{{ liItem.resolution }}</span>
                  <a class="jsAnchor overlay-anchor wall-favs"
                     data-href="https://wallhaven.cc/wallpaper/fav/x8kwd3">{{
                      this.$formatFileSize(liItem.file_size)
                    }}</a>
                  <span v-if="liItem.file_type === 'png'" class="png"><span>PNG</span></span>
                  <a class="jsAnchor thumb-tags-toggle delete-btn" title="删除" @click="deleteFile(i,index)">
                    <i class="fas fa-fw fa-trash"></i>
                  </a>
                </div>
              </figure>
            </li>
          </ul>
        </section>
      </div>
      <div class="main-bottom">
        <div class="loading-span" v-show="loading"><i class="fas fa-spinner"></i></div>
        <div class="error-span" v-show="error"><i class="fas fa-times"> <br/>请求异常</i></div>
      </div>
    </main>
  </div>
</template>

<script>
import imgPreview from "../components/img_preview.vue";
import pageHeader from "../components/page-header.vue";
import {changeBg, getLocalData, deleteFile} from "../statics/js/ipcRenderer"

export default {
  name: "switchList",
  data() {
    return {
      title: "本地列表",
      showImgPre: false,
      preImgInfo: {},
      loading: false,
      error: false,
      pageData: {
        totalPage: 0,
        currentPage: 0,
        sections: []
      }
    }
  },
  created: function () {
    this.loading = true;
    this.getNextPage();
  },
  mounted() {
    // 添加滚动事件，检测滚动到页面底部
    window.addEventListener('scroll', this.scrollEvent)
  },
  unmounted() {
    // 移除滚动事件
    window.removeEventListener('scroll', this.scrollEvent)
  },
  components: {
    imgPreview,
    pageHeader
  },
  methods: {
    closePreview(value) {
      this.preImgInfo = {};
      this.showImgPre = value;
    },
    preview(imgItem) {
      this.showImgPre = true;
      this.preImgInfo = {
        "realPath": imgItem.path,
        "path": imgItem.base64
      }
    },
    deleteFile(sectionIndex, index) {
      const item = this.pageData.sections[sectionIndex][index]
      deleteFile(item.path).then(res => {
        this.$message({
          message: res.msg,
          type: res.type,
          duration: res.type === "success" ? 1200 : 2000,
          customClass: 'customer-message'
        })
        if(res.success){
          this.pageData.sections[sectionIndex].splice(index,1)
        }
      })
    },
    getNextPage() {
      this.pageData.currentPage++;
      this.loading = true;
      this.error = false
      let params = {
        'page': this.pageData.currentPage,
        'size': 24
      }
      getLocalData(params).then(res => {
        this.pageData.totalPage = res.totalPage;
        this.pageData.sections.push(res.data);
        this.$nextTick(() => {
          this.loading = false;
        });
      }).catch(err => {
        this.$nextTick(() => {
          this.loading = false;
        });
        this.error = true
      })
    },
    scrollEvent() {
      if (document.body.scrollHeight - document.documentElement.scrollTop - document.body.clientHeight <= 200 &&
          !this.loading && this.pageData.currentPage < this.pageData.totalPage) {
        this.getNextPage();
      }
    },
    setBg(imgInfo) {
      let imgInfoCopy = {
        "url": imgInfo.path
      }
      changeBg(imgInfoCopy).then(res => {
        this.$message({
          message: res.msg,
          type: res.type,
          duration: res.type === "success" ? 1200 : 2000,
          customClass: 'customer-message'
        })
      })
    }
  }
}
</script>

<style scoped>
@import url("../statics/css/all.css");
@import url("../statics/css/list.css");

#thumbs {
  padding-top: 10px;
}

.delete-btn{
  color: #cc4433 !important;
}

#main {
  padding-top: 40px;
}

.main-bottom {
  height: 30px;
  text-align: center;
}

.loading-span {
  width: 30px;
  height: 30px;
  margin: 0 auto;
}

.error-span i {
  font-size: 18px !important;
}

.fa-spinner {
  animation: spin 0.8s infinite linear;
}

.main-bottom i {
  font-size: 30px;
  line-height: 1.2;
  font-weight: normal !important;
}
</style>
