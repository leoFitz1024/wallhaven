<template>
  <imgPreview @close="closePreview" :showing="showImgPre" :imgInfo="preImgInfo"></imgPreview>
  <div id="WallHaven">
    <pageHeader :title="title"></pageHeader>
    <form id="searchbar" class="expanded" @click="resetSelect">
      <div @click.stop="" id="search-keyword" class="framed searchbar-dropdown">
        <input type="text" name="keyword" placeholder="搜索关键词（英文）" v-model="customParams.keyword"/>
      </div>
      <div @click.stop="" id="search-category-checks" class="framed">
        <input type="checkbox" v-model="customParams.categories" name="general" value="general"
               id="search-general"/>
        <label for="search-general">普通</label>
        <input type="checkbox" v-model="customParams.categories" name="anime" value="anime" id="search-anime"/>
        <label for="search-anime">动漫</label>
        <input type="checkbox" v-model="customParams.categories" name="people" value="people"
               id="search-people"/>
        <label for="search-people">人物</label>
      </div>
      <div @click.stop="" id="search-aiart-checks" class="framed">
        <input type="checkbox" v-model="customParams.aiArt" value=true name="ai_art_filter"
               id="search-ai">
        <label for="search-ai">AI画作</label>
      </div>
      <div @click.stop="" id="search-purity-checks" class="framed">
        <input type="checkbox" v-model="customParams.purity" name="sfw" value="sfw" id="search-sfw"/>
        <label class="purity sfw" for="search-sfw" title="正经图">SFW</label>
        <input type="checkbox" v-model="customParams.purity" name="sketchy" value="sketchy"
               id="search-sketchy"/>
        <label class="purity sketchy" for="search-sketchy" title="带点颜色">Sketchy</label>
        <input v-show="apiKey !== ''" type="checkbox" v-model="customParams.purity" name="nsfw" value="nsfw"
               id="search-nsfw"/>
        <label v-show="apiKey !== ''" class="purity nsfw" for="search-nsfw" title="开车图">NSFW</label>
      </div>
      <div @click.stop="" id="search-resolutions" class="framed searchbar-dropdown">
        <a class="jsAnchor dropdown-toggle" :class=" customParams.selector === 1 ? 'extended' : 'collapsed'"
           @click="changeSelector(1)">分辨率</a>
        <div class="dropdown " :class=" customParams.selector === 1 ? 'extended' : 'collapsed'">
          <div>
            <div class="framed">
              <input type="radio" v-model="customParams.respickerLimitation"
                     name="searchbar-respicker-limitation" id="searchbar-respicker-atleast"
                     value="atleast"/>
              <label for="searchbar-respicker-atleast"> <i class="far fa-plus"></i> 至少 </label>
              <input type="radio" v-model="customParams.respickerLimitation"
                     name="searchbar-respicker-limitation" id="searchbar-respicker-exactly"
                     value="exactly"/>
              <label for="searchbar-respicker-exactly"><i class="far fa-dot-circle"></i> 精确的 </label>
            </div>
            <div class="respicker">
              <p v-show="desktopInfo !== ''" class="respicker-native-info">
                你的屏幕分辨率：<strong><em>{{ this.$root.desktopInfo }}</em></strong>.</p>
              <table class="label-table">
                <thead>
                <tr>
                  <th>Ultrawide</th>
                  <th>16:9</th>
                  <th>16:10</th>
                  <th>4:3</th>
                  <th>5:4</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(line, i) in searchMeta.resolutionsArray">
                  <td v-for="(rln, x) in line.item">
                    <input v-if="customParams.respickerLimitation !== 'atleast'" type="checkbox"
                           name="respicker-resolution" :id="'searchbar-respicker-' + (rln)"
                           :value="rln" v-model="customParams.resolutions"/>
                    <input v-if="customParams.respickerLimitation === 'atleast'" type="radio"
                           name="respicker-resolution" :id="'searchbar-respicker-' + (rln)"
                           :value="rln" v-model="customParams.resolution"/>
                    <label :for="'searchbar-respicker-' + (rln)"
                           original-title="Dual 1080p">{{ this.$formatMulti(rln) }}</label>
                  </td>
                </tr>
                </tbody>
              </table>
              <hr/>
              <div class="respicker-custom oneline framed">
                <label for="searchbar-respicker-custom-width">自定义分辨率</label>
                <input type="text" pattern="[0-9]{0,5}" v-model="customParams.respickerCustomWidth"
                       name="respicker-custom-width" id="searchbar-respicker-custom-width"
                       placeholder="Width" maxlength="5"/>
                <label class="respicker-custom-separator"><i class="far fa-times"></i></label>
                <input type="text" pattern="[0-9]{0,5}" v-model="customParams.respickerCustomHeight"
                       name="respicker-custom-height" id="searchbar-respicker-custom-height"
                       placeholder="Height" maxlength="5"/>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div @click.stop="" id="search-ratios" class="framed searchbar-dropdown">
        <a class="jsAnchor dropdown-toggle" :class=" customParams.selector === 2 ? 'extended' : 'collapsed'"
           @click="changeSelector(2)" style="min-width: 5em">比例</a>
        <div class="dropdown" :class=" customParams.selector === 2 ? 'extended' : 'collapsed'">
          <div style="padding: .5em 1em;">
            <div class="respicker">
              <table class="label-table">
                <thead>
                <tr>
                  <th>宽屏</th>
                  <th>超宽屏</th>
                  <th>竖屏</th>
                  <th>方屏</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                  <td colspan="2">
                    <input type="checkbox" name="ratio" v-model="customParams.ratios" value="landscape" class="ratio"
                           id="searchbar-ratio-landscape"/>
                    <label for="searchbar-ratio-landscape"> 全部横屏 </label>
                  </td>
                  <td><input type="checkbox" name="ratio" v-model="customParams.ratios" value="portrait" class="ratio"
                             id="searchbar-ratio-portrait"/><label for="searchbar-ratio-portrait">全部竖屏</label></td>
                </tr>
                <tr v-for="(line,i) in searchMeta.ratiosArray">
                  <td v-for="(ra,x) in line.item">
                    <input v-if="ra !== ''" v-model="customParams.ratios" type="checkbox"
                           name="ratio" :value="ra" class="ratio"
                           :id="'searchbar-ratio-' + (ra)"/>
                    <label :for="'searchbar-ratio-' + (ra)">{{ this.$formatMulti(ra) }}</label>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div @click.stop="" id="search-colors" class="framed searchbar-dropdown">
        <a class="jsAnchor dropdown-toggle" :class=" customParams.selector === 3 ? 'extended' : 'collapsed'"
           @click="changeSelector(3)" style="border-radius: 3px;"
           :style="customParams.color !== 'none' ? 'background-color: #' + (customParams.color) + ';' : ''">颜色</a>
        <div class="dropdown" :class=" customParams.selector === 3 ? 'extended' : 'collapsed'">
          <div style="padding: .5em 1em;">
            <div class="colorpicker">
              <table class="label-table">
                <tbody>
                <tr v-for="(line, i) in searchMeta.colorsArray">
                  <td v-for="(colorItem, i) in line.item">
                    <input type="radio" v-model="customParams.color" name="search-colors"
                           :id="'search-colors-' + (colorItem)" :value="colorItem"/>
                    <label :for="'search-colors-' + (colorItem)"
                           :style="colorItem === 'none' ? 'height: 2em;background:linear-gradient(18deg, rgba(255,255,255,1) 42%,rgba(255,0,0,1) 45%,rgba(255,0,0,1) 55%,rgba(255,255,255,1) 58%);' : 'background: #' + (colorItem)+'; height: 2em;'">
                    </label>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div @click.stop="" id="search-sorting" class="framed searchbar-dropdown">
        <input type="checkbox" name="order" v-model="customParams.desc" value="desc" id="search-order"/>
        <label for="search-order" original-title="Ascending/Descending"></label>
        <a class="jsAnchor dropdown-toggle" :class=" customParams.selector === 4 ? 'extended' : 'collapsed'"
           @click="changeSelector(4)" style="width: 7em">{{ sortingFormat(customParams.sorting) }}</a>
        <div class="dropdown" :class=" customParams.selector === 4 ? 'extended' : 'collapsed'">
          <div>
            <input type="radio" v-model="customParams.sorting" name="sorting" value="relevance"
                   id="search-sorting-relevance"/>
            <label for="search-sorting-relevance">相关性</label>
            <input type="radio" v-model="customParams.sorting" name="sorting" value="random"
                   id="search-sorting-random"/>
            <label for="search-sorting-random">随机</label>
            <input type="radio" v-model="customParams.sorting" name="sorting" value="date_added"
                   id="search-sorting-date"/>
            <label for="search-sorting-date">日期</label>
            <input type="radio" v-model="customParams.sorting" name="sorting" value="views"
                   id="search-sorting-views"/>
            <label for="search-sorting-views">浏览量</label>
            <input type="radio" v-model="customParams.sorting" name="sorting" value="favorites"
                   id="search-sorting-favorites"/>
            <label for="search-sorting-favorites">收藏数</label>
            <input type="radio" v-model="customParams.sorting" name="sorting" value="toplist"
                   id="search-sorting-toplist">
            <label for="search-sorting-toplist">排行榜</label>
            <input type="radio" v-model="customParams.sorting" name="sorting" value="hot"
                   id="search-sorting-hot"/>
            <label for="search-sorting-hot">热度</label>
          </div>
        </div>
      </div>
      <div @click.stop="" :style="customParams.sorting !== 'toplist' ? 'visibility:hidden' : ''"
           id="search-toplist-range"
           class="framed searchbar-dropdown">
        <a class="jsAnchor dropdown-toggle" :class=" customParams.selector === 5 ? 'extended' : 'collapsed'"
           @click="changeSelector(5)" style="width: 8.5em;">{{ topRangeFormat(customParams.topRange) }}</a>
        <div class="dropdown" :class=" customParams.selector === 5 ? 'extended' : 'collapsed'">
          <div>
            <input type="radio" v-model="customParams.topRange" name="top" value="1d"
                   id="searchbar-toplist-range-1d"/>
            <label for="searchbar-toplist-range-1d">1 天</label>
            <input type="radio" v-model="customParams.topRange" name="top" value="3d"
                   id="searchbar-toplist-range-3d"/>
            <label for="searchbar-toplist-range-3d">3 天</label>
            <input type="radio" v-model="customParams.topRange" name="top" value="1w"
                   id="searchbar-toplist-range-1w"/>
            <label for="searchbar-toplist-range-1w">上周</label>
            <input type="radio" v-model="customParams.topRange" name="top" value="1M"
                   id="searchbar-toplist-range-1M" checked=""/>
            <label for="searchbar-toplist-range-1M">1 个月</label>
            <input type="radio" v-model="customParams.topRange" name="top" value="3M"
                   id="searchbar-toplist-range-3M"/>
            <label for="searchbar-toplist-range-3M">3 个月</label>
            <input type="radio" v-model="customParams.topRange" name="top" value="6M"
                   id="searchbar-toplist-range-6M"/>
            <label for="searchbar-toplist-range-6M">6 个月</label>
            <input type="radio" v-model="customParams.topRange" name="top" value="1y"
                   id="searchbar-toplist-range-1y"/>
            <label for="searchbar-toplist-range-1y">去年</label>
          </div>
        </div>
      </div>
      <button type="button" class="button" id="search-submit" @click="changeParams"><i class="fas fa-sync"></i></button>
      <el-tooltip content="设置为在线切换模式参数" placement="bottom" effect="light" popper-class="custom-tips">
        <button type="button" class="button" id="search-save" @click="saveParams"><i class="fas"
                                                                                     :class=" saving ? 'fa-spinner' : 'fa-save'"></i>
        </button>
      </el-tooltip>
    </form>
    <main id="main" @click="resetSelect">
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
              <figure class="thumb"
                      :class="'thumb-' + (liItem.id) + ' thumb-' + (liItem.purity) + ' thumb-' + (liItem.category)"
                      :data-wallpaper-id="liItem.id" style="width:300px;height:200px">
                <a class="thumb-btn thumb-btn-fav jsAnchor overlay-anchor" title="设为壁纸" @click="setBg(liItem)">
                  <i class="fas fa-fw fa-repeat-alt"></i>
                </a>
                <img alt="loading" loading="lazy" class="lazyload loaded"
                     :data-src="liItem.thumbs.small" :src="liItem.thumbs.small"/>
                <a class="preview" @click="preview(liItem)"></a>
                <div class="thumb-info">
                  <span class="wall-res">{{ this.$formatMulti(liItem.resolution) }}</span>
                  <a class="jsAnchor overlay-anchor wall-favs">{{ this.$formatFileSize(liItem.file_size) }}</a>
                  <span v-if="liItem.file_type === 'image/png'" class="png"><span>PNG</span></span>
                  <a class="jsAnchor thumb-tags-toggle tagged" title="下载" @click="downloadImg(liItem)">
                    <i class="fas fa-fw fa-download"></i>
                  </a>
                </div>
              </figure>
            </li>
          </ul>
        </section>
      </div>
      <div class="main-bottom">
        <div class="loading-span" v-show="loading"><i class="fas fa-spinner"></i></div>
        <div class="error-span" v-show="error"><i class="fas fa-times"> <br/>网络异常，请点击右上角刷新按钮重试。</i></div>
      </div>
    </main>
  </div>
</template>

<script>
import {updatePageParams, changeBg} from "../statics/js/ipcRenderer"
import imgPreview from "../components/img_preview.vue";
import pageHeader from "../components/page-header.vue";
import {ElTooltip} from 'element-plus'
import {getLocalStorage} from "../statics/js/utils"

const ALL_CATEGORIES = ['general', 'anime', 'people']
const ALL_PURITY = ['sfw', 'sketchy', 'nsfw']

export default {
  name: "onlineWall",
  data() {
    return {
      saving: false,
      title: "在线壁纸",
      isCurrent: false,
      showImgPre: false,
      preImgInfo: {},
      loading: false,
      error: false,
      apiKey: "",
      getParams: {
        q: "",
        ai_art_filter: 0,
        categories: 111,
        purity: 100,
        sorting: "hot",
        topRange: "1M",
        order: "desc",
        colors: null,
        ratios: "",
        atleast: null,
        resolutions: null,
        page: 1,
      },
      customParams: {
        selector: 0,
        keyword: "",
        categories: ["general", "anime", "people"],
        aiArt: false,
        purity: ["sfw"],
        sorting: "hot",
        desc: true,
        topRange: "1M",
        ratios: [],
        respickerLimitation: "exactly",
        resolutions: [],
        resolution: "",
        respickerCustomWidth: "",
        respickerCustomHeight: "",
        color: 'none',
      },
      searchMeta: {
        resolutionsArray: [{
          item: ['2560x1080', '1280x720', '1280x800', '1280x960', '1280x1024']
        },
          {
            item: ['3440x1440', '1600x900', '1600x1000', '1600x1200', '1600x1280']
          },
          {
            item: ['3840x1600', '1920x1080', '1920x1200', '1920x1440', '1920x1536']
          },
          {
            item: ['2560x1440', '2560x1600', '2560x1920', '2560x2048']
          },
          {
            item: ['3840x2160', '3840x2400', '3840x2880', '3840x3072']
          }
        ],
        ratiosArray: [{
          item: ['16x9', '21x9', '9x16', '1x1']
        },
          {
            item: ['16x10', '32x9', '10x16', '3x2']
          },
          {
            item: ['', '48x9', '9x18', '4x3']
          },
          {
            item: ['', '', '', '5x4']
          },
        ],
        colorsArray: [{
          item: ['660000', '990000', 'cc0000', 'cc3333', 'ea4c88', '993399']
        },
          {
            item: ['663399', '333399', '0066cc', '0099cc', '66cccc', '77cc33']
          },
          {
            item: ['669900', '336600', '666600', '999900', 'cccc33', 'ffff00']
          },
          {
            item: ['ffcc33', 'ff9900', 'ff6600', 'cc6633', '996633', '663300']
          },
          {
            item: ['000000', '999999', 'cccccc', 'ffffff', '424153', 'none']
          },
        ]
      },
      pageData: {
        totalPage: 0,
        currentPage: 0,
        sections: []
      }
    }
  },
  props: ['desktopInfo'],
  watch: {
    'customParams.categories': {
      handler: function () {
        if (this.customParams.categories.length === 0) {
          this.customParams.categories.push("general")
          this.customParams.categories.push("anime")
        }
        this.scrollEvent()
      }
    }
  },
  created: function () {
    this.isCurrent = true
    let customParamsJson = getLocalStorage("customParams", "{}", "String")
    this.initParams(JSON.parse(customParamsJson))
    this.loading = true
    this.formatGetParams()
    this.getNextPage()
  },
  mounted() {
    // 添加滚动事件，检测滚动到页面底部
    window.addEventListener('scroll', this.scrollEvent)
    this.apiKey = localStorage.getItem("apiKey")
  },
  unmounted() {
    // 移除滚动事件
    window.removeEventListener('scroll', this.scrollEvent)
    this.isCurrent = false
  },
  components: {
    pageHeader,
    imgPreview,
    ElTooltip
  },
  methods: {
    resetSelect() {
      this.customParams.selector = 0
    },
    changeSelector(index) {
      this.customParams.selector = this.customParams.selector === index ? 0 : index;
    },
    closePreview(value) {
      this.preImgInfo = {}
      this.showImgPre = value;
    },
    preview(imgItem) {
      this.preImgInfo = imgItem
      this.showImgPre = true;
    },
    downloadImg(imgItem) {
      let info = {
        "id": imgItem.id,
        "url": imgItem.path,
        "size": imgItem.file_size,
        "small": imgItem.thumbs.small,
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
    },
    setBg(imgItem) {
      let info = {
        "id": imgItem.id,
        "url": imgItem.path,
        "size": imgItem.file_size,
        "small": imgItem.thumbs.small,
        "resolution": imgItem.resolution
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
    changeParams() {
      this.pageData.sections.length = 0;
      this.pageData.currentPage = 0;
      this.customParams.selector = 0;
      if (this.customParams.categories.length === 0) {
        this.customParams.categories = ["general", "anime"];
      }
      if (this.customParams.purity.length === 0) {
        this.customParams.purity = ["sfw"]
      }
      localStorage.setItem("customParams", JSON.stringify(this.customParams))
      this.formatGetParams();
      this.getNextPage();
    },
    saveParams() {
      this.saving = true
      this.formatGetParams();
      let apiParams = this.getApiParamStr(this.getParams, true)
      localStorage.setItem('apiParams', apiParams)
      updatePageParams(apiParams).then(res => {
        this.$message({
          message: res.msg,
          type: res.type,
          duration: res.type === "success" ? 1200 : 2000,
          customClass: 'customer-message'
        })
      }).finally(() => {
        this.saving = false
      })
    },
    formatGetParams() {
      this.getParams = {
        q: "",
        ai_art_filter: 0,
        categories: 111,
        purity: 100,
        sorting: "hot",
        topRange: "1M",
        order: "desc",
        colors: null,
        ratios: "",
        atleast: null,
        resolutions: null,
        page: 1,
      };
      this.getParams.q = this.customParams.keyword;
      this.getParams.ai_art_filter = this.customParams.aiArt ? 0 : 1;
      this.getParams.categories = this.formatCategory();
      this.getParams.purity = this.formatPurity();
      this.getParams.sorting = this.customParams.sorting;
      this.getParams.topRange = this.customParams.topRange;
      this.getParams.order = this.customParams.desc ? "desc" : "asc";
      this.getParams.colors = this.customParams.color === 'none' ? null : this.customParams.color;
      let ratiosStr = this.customParams.ratios.join(',');
      this.getParams.ratios = ratiosStr === "" ? null : ratiosStr;
      if (this.customParams.respickerCustomWidth !== "" && this.customParams.respickerCustomHeight !==
          "") {
        this.getParams.atleast = this.customParams.respickerCustomWidth + "x" + this.customParams
            .respickerCustomHeight;
        this.customParams.resolutions.push(this.getParams.atleast);
      }
      if (this.customParams.respickerLimitation === "atleast") {
        if (this.customParams.resolution !== "" && this.getParams.atleast != null) {
          this.getParams.atleast = this.customParams.resolution;
        }
      } else {
        this.getParams.atleast = null;
        let resolutionsStr = this.customParams.resolutions.join(",");
        this.getParams.resolutions = resolutionsStr === "" ? null : resolutionsStr;
      }
    },
    getNextPage() {
      this.pageData.currentPage++;
      this.getParams.page = this.pageData.currentPage;
      this.loading = true;
      this.error = false;
      let apiParams = this.getApiParamStr(this.getParams)
      let apiKey = getLocalStorage("apiKey", "", "String");
      if (apiKey !== "") {
        apiParams = `${apiParams}&apikey=${apiKey}`
      }
      this.$wallhavenApi.search(apiParams).then(res => {
        this.pageData.currentPage = res.meta['current_page'];
        this.pageData.totalPage = res.meta['last_page'];
        this.pageData.sections.push(res.data);
        this.$nextTick(() => {
          this.loading = false;
          this.scrollEvent()
        });
      }).catch(err => {
        console.log("请求数据失败：" + err)
        this.$nextTick(() => {
          this.loading = false;
        });
        this.error = true
      })

    },
    getApiParamStr(getParams, clearPage = false) {
      return Object.keys(getParams).filter(function (key) {
        if ((clearPage && key === "page") || encodeURIComponent(getParams[key]) === 'null') {
          return false
        } else {
          return true
        }
      }).map(function (key) {
        return encodeURIComponent(key) + "=" + encodeURIComponent(getParams[key])
      }).join("&");
    },
    //初始化参数，去除失效的参数，增加初始化新增的参数
    initParams(oldCustomParams) {
      let that = this;
      Object.keys(this.customParams).forEach(function (key) {
        that.customParams[key] = oldCustomParams[key] == null ? that.customParams[key] : oldCustomParams[key]
      })
    },
    scrollEvent() {
      this.$nextTick(() => {
        if (document.body.scrollHeight - document.documentElement.scrollTop - document.body.clientHeight <= 200 &&
            !this.loading && this.pageData.currentPage < this.pageData.totalPage && this.isCurrent) {
          this.getNextPage();
        }
      });

    },
    formatCategory() {
      return ALL_CATEGORIES.map(cat => {
        return String(Number(this.customParams.categories.indexOf(cat) > -1))
      }).join('')
    },
    formatPurity() {
      return ALL_PURITY.map(cat => {
        return String(Number(this.customParams.purity.indexOf(cat) > -1))
      }).join('')
    },
    sortingFormat(sorting) {
      switch (sorting) {
        case "relevance":
          sorting = "相关性";
          break;
        case "random":
          sorting = "随机";
          break;
        case "date_added":
          sorting = "日期";
          break;
        case "views":
          sorting = "浏览量";
          break;
        case "favorites":
          sorting = "收藏数";
          break;
        case "toplist":
          sorting = "排行榜";
          break;
        case "hot":
          sorting = "热度";
          break;
        default:
          sorting = "排行榜";
      }
      return sorting;
    },
    topRangeFormat(topRange) {
      switch (topRange) {
        case "1d":
          topRange = "1 天";
          break;
        case "3d":
          topRange = "3 天";
          break;
        case "1w":
          topRange = "上周";
          break;
        case "1M":
          topRange = "1 个月";
          break;
        case "3M":
          topRange = "3 个月";
          break;
        case "6M":
          topRange = "6 个月";
          break;
        case "1y":
          topRange = "去年";
          break;
        default:
          topRange = "上周";
      }
      return topRange;
    }
  }
}
</script>

<style scoped>
@import url("../statics/css/list.css");

#search-save {
  /*background-color: #777744 !important;*/
  background-image: linear-gradient(to bottom, #d5bf2a 0, #777744 100%) !important;
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

#WallHaven::-webkit-scrollbar {
  display: none;
}


</style>
