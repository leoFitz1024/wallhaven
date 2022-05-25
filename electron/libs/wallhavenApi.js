const axios = require('axios');

const ALL_CATEGORIES = ['general', 'anime', 'people']

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

    /**
     * 检查apikey是否合法
     */
    checkApiKey(apikey) {
        return new Promise((resolve, reject) => {
            if(apikey !== ""){
                this.myCollections(apikey).then(res => {
                    resolve(true)
                }).catch((e) => {
                    resolve(false)
                })
            }else{
                resolve(false)
            }
        })
    }

    request(params, page) {
        params = params + "&page=" + page
        if (this.apikey !== null && this.apikey !== "") {
            params = params + "&apikey=" + this.apikey
        }
        return request(this.apiPrefix + "/search?" + params)
    }


}
