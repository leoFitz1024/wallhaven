<template>
  <header id="header">
    <label>{{ title }}</label>
    <div class="win-btn-wrap">
      <span class="win-btn min-btn"><i class="fas fw fa-window-minimize" @click="minimize"></i></span>
      <span class="win-btn max-btn"><i class="fas fw fa-window-maximize" @click="maximize"></i></span>
      <span class="win-btn close-btn"><i class="fas fw fa-window-close" @click="close"></i></span>
    </div>
  </header>
</template>

<script>
import { minWindow, maxWindow, closeWindow } from "../statics/js/ipcRenderer"

export default {
  name: "pageHeader",
  data() {
    return {}
  },
  methods: {
    minimize(){
      minWindow()
    },
    maximize(){
      maxWindow()
    },
    close(){
      localStorage.setItem("downloadList", JSON.stringify(this.$root.downloadList))
      localStorage.setItem("downloadFinishedList", JSON.stringify(this.downloadFinishedList))
      closeWindow()
    }
  },
  props: {
    title: ""
  },
}
</script>

<style scoped>

.win-btn-wrap{
  height: 40px;
  display: inline-block;
  position: fixed;
  z-index: 999;
  right: 10px;
}

.win-btn{
  -webkit-app-region: no-drag;
  display: inline-block;
  margin: 10px 15px 0 15px;
  cursor:pointer;
}

.min-btn{
  margin-top: 2px;
  /*padding-bottom: 15px;*/
}

#header {
  -webkit-app-region: drag;
  cursor:move !important;
  position: fixed;
  top: 0;
  height: 40px;
  width: 100%;
  min-width: 640px;
  z-index: 200
}

@media (max-width: 639px) {
  #header {
    position: absolute;
    min-width: 800px
  }
}

#header {
  color: #FFF;
  justify-content: center;
  -ms-flex-align: center;
  align-items: center;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  font-size: 1.2em;
  white-space: nowrap;
  background-color: rgb(58 56 56 / 27%);
  background-image: linear-gradient(to bottom, #787a7c4f 0, #3f414247 100%);
  text-shadow: 1px 1px 3px rgba(0, 0, 0, .75);
  box-shadow: inset 0 0 0 1px rgba(31, 31, 31, .66), 0 0 0px rgba(0, 0, 0, 0), 0 0 10px rgba(0, 0, 0, .75)
}

#header label {
  margin-right: 230px;
}
</style>
