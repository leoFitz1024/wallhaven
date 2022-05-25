<template>
  <div class="mask" :class="showing === true ? '' : 'out'">
    <a class="close_btn" @click="close"></a>
    <div class="img-view">
      <img class="img-class" :src="imgInfo.path" :style="{'max-height':calHeight}">
      <img class="img-class close-bg" v-show="!showing" :src="imgBgSrc" :style="{'max-height':calHeight}">
    </div>
    <div class="sidebar-fixed-wrapper" style="bottom: 40px;">
      <div class="details-sidebar-fixed-box hi-de">
        <div class="sidebar-fixed_box comments-middle-icon" title="设为壁纸" @click="setBg(imgInfo)">
          <div class="icon-wrap"><i class="fas fa-repeat-alt"></i></div>
        </div>
        <div v-show="!isLocal" class="sidebar-fixed_box share-middle-icon sidebar-share" title="下载"
             @click="downloadImg(imgInfo)">
          <div class="icon-wrap"><i class="fas fa-download"></i></div>
        </div>
      </div>
      <div class="back-to-top sidebar-fixed_box" z-st="shortcut_totop" style="display: block;"></div>
    </div>
  </div>
</template>

<script>
import {changeBg} from "../statics/js/ipcRenderer";

export default {
  name: "imgPreview",
  data() {
    return {
      isLocal: false,
      clientHeight: 1080,
      imgBgSrc: ""
    }
  },
  props: {
    showing: false,
    imgInfo: {}
  },
  mounted() {
    this.clientHeight = document.documentElement.clientHeight;
    window.addEventListener('resize', this.onresize);
  },
  methods: {
    onresize() {
      if (document.documentElement.clientHeight !== undefined) {
        this.clientHeight = document.documentElement.clientHeight;
      }
    },
    close() {
      this.imgBgSrc = this.imgInfo.path;
      this.isLocal = false
      this.$emit('close', false)
    },
    setBg(imgItem) {
      let info;
      if(this.isLocal){
        info = {
          "url": imgItem.realPath
        }
      }else{
        info = {
          "id": imgItem.id,
          "url": imgItem.path,
          "size": imgItem['file_size'],
          "small": imgItem['thumbs'].small,
          "resolution": imgItem.resolution
        }
      }
      changeBg(info).then(res => {
        this.$message({
          message: res.msg,
          type: res.type,
          duration: res.type === "success" ? 1200 : 2000,
          customClass: 'customer-message'
        })
      })
    },
    downloadImg(imgItem) {
      let info = {
        "id": imgItem.id,
        "url": imgItem.path,
        "size": imgItem['file_size'],
        "small": imgItem['thumbs'].small,
        "resolution": imgItem.resolution
      }
      this.$root.addDownloadFile(info).then(res => {
        this.$message({
          message: res.msg,
          type: res.type,
          duration: res.type === "success" ? 1200 : 2000,
          customClass: 'customer-message'
        })
      })
    }
  },
  computed: {
    calHeight() {
      return parseInt(this.clientHeight * 0.9) + "px";
    }
  },
  watch: {
    imgInfo(value) {
      if (this.imgInfo.realPath !== undefined) {
        this.isLocal = true
      }
    }
  }
}
</script>

<style scoped>
.close_btn {
  z-index: 999;
  display: none;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  position: absolute;
  top: 20px;
  right: 40px;
  text-decoration: none;
  background: url(../statics/icons/icon-s-close-hover.svg) center no-repeat #222;
}

.sidebar-fixed-wrapper {
  color: #000000;
  position: fixed;
  right: 40px;
  bottom: 40px;
  z-index: 999;
  visibility: hidden;
}

.comments-middle-icon,
.share-middle-icon {
  border: 1px solid #E9E9E9;
  background-color: #222;
  -webkit-transition: background .3s;
  transition: background .3s;
}

.icon-wrap {
  position: relative;
  top: 12px;
  width: 21px;
  margin: 0 auto;
  color: #d7ce82;
}

.sidebar-fixed-wrapper .sidebar-fixed_box {
  color: #d3dce6;
  width: 50px;
  height: 50px;
  margin-top: 10px;
  cursor: pointer;
  border: none;
  position: relative;
  background-repeat: no-repeat;
  background-position: center;
  border-radius: 4px;
  font-size: 20px;
}


.img-class {
  object-fit: cover;
  max-width: 95%;
}


.mask {
  z-index: 999;
  width: 100%;
  height: 100%;
  position: fixed;
  margin: auto;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.88);
  -webkit-user-select: none;
  /*谷歌 /Chrome*/
  -moz-user-select: none;
  /*火狐/Firefox*/
  -ms-user-select: none;
  /*IE 10+*/
  user-select: none;
  /* background-color: rgba(103, 103, 103, 0.5); */
  display: table;
}

.mask.out {
  opacity: 0;
  visibility: hidden
}

.mask:hover .close_btn {
  display: inline-block;
}

.mask:hover .sidebar-fixed-wrapper {
  visibility: visible;
}

.img-view {
  text-align: center;
  display: table-cell;
  vertical-align: middle;
  width: auto;
  margin-left: auto;
}

.img-class {
  margin: 0 auto;
}

.img-view > img {
  border-radius: 3px;
  box-shadow: 0 1px 1px 1px #222, 5px 5px 5px rgb(84 84 84 / 50%);
}


/*弹层动画（放大）*/
.mask {
  transition: all 0.3s;
  -moz-transition: all 0.3s;
  /* Firefox 4 */
  -webkit-transition: all 0.3s;
  /* Safari and Chrome */
  -o-transition: all 0.3s;
  /* Opera */
  visibility: visible;
  opacity: 1;
  transform: scale(1);
}

.mask .img-view .img-class {
  animation: blowUpModal 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
}

.mask.out .img-view .img-class {
  animation: blowUpModalTwo 0.5s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
}


@keyframes blowUpModal {
  0% {
    transform: scale(0);
  }

  100% {
    transform: scale(1);
  }
}

@keyframes blowUpModalTwo {
  0% {
    transform: scale(1);
    opacity: 1;
  }

  100% {
    transform: scale(0);
    opacity: 0;
  }
}
</style>
