import axios from './axios';
import API_IPC from "../../../electron/common/apiIPC"
import {getLocalStorage} from "./utils";

export default {

    init(){
        window.ipcRenderer.on(API_IPC.SEARCH, (params) => {
            this.search(params).then(res => {
                window.ipcRenderer.send(API_IPC.SEARCH, res)
            })
        })
    },
    /**
     * 查找
     */
    search(params){
        let apiKey = getLocalStorage("apiKey", "", "String")
        if (apiKey !== ""){
            params = `${params}&apiKey=${apiKey}`
        }
        return axios.get(`/search?${params}`, {})
    }
}
