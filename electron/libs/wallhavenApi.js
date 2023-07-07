const AXIOS = require('axios');
const LOGGER = require("../logger");

const ALL_CATEGORIES = ['general', 'anime', 'people']

let axios = AXIOS.create({
    timeout:10000,
    headers:{
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'
    },
    proxy: undefined
})

function request(url) {
    return axios.get(url)
}

function getCategories(categories) {
    return ALL_CATEGORIES.map(cat => {
        return String(Number(categories.indexOf(cat) > -1))
    }).join('')
}

function getResolution(text) {
    return text.split('x').map(v => Number(v.trim()))
}

module.exports = class WallhavenApi {

    constructor() {
        this.apiPrefix = "https://wallhaven.cc/api/v1"
        this.apikey = null
    }

    /**
     * 设置代理
     */
    setProxy(proxyServer){
        axios = AXIOS.create({
            timeout:10000,
            headers:{
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'
            },
            proxy: {
                "host": proxyServer.address,
                "port": proxyServer.port,
                "protocol": proxyServer.protocol,
            }
        })
    }

    /**
     * 清除代理
     */
    clearProxy(){
        axios = AXIOS.create({
            timeout:10000,
            headers:{
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'
            }
        })
    }

    /**
     * 设置apiKey
     */
    setApikey(apikey) {
        if(apikey !== ""){
            this.apikey = apikey
        }
    }

    search(keyword = '', {
        categories = ALL_CATEGORIES,
        page = 1,
        sorting = 'relevance',
        nsfw = false,
        sketchy = false
    } = {}) {
        keyword = encodeURIComponent(keyword)
        categories = getCategories(categories)
        const purity = `1${Number(sketchy)}${Number(!nsfw)}`
        let url = `${this.apiPrefix}/search?q=${keyword}&categories=${categories}&purity=${purity}&sorting=${sorting}&page=${page}&order=desc`
        if (this.apikey && this.apikey !== "") {
            url = `${url}&apikey=${this.apikey}`
        }
        return request(url)
    }

    myCollections(apikey = this.apikey) {
        let s = `${this.apiPrefix}/collections?apikey=${apikey}`;
        return request(s)
    }

    request(params, page) {
        params = params + "&page=" + page
        if (this.apikey !== null && this.apikey !== "") {
            params = params + "&apikey=" + this.apikey
        }
        const url = this.apiPrefix + "/search?" + params;
        LOGGER.info("api request:" + url)
        return request(url)
    }
}
