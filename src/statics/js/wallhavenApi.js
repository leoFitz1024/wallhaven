import axios from './axios';
import API_IPC from "../../../electron/common/apiIPC"

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
        return axios.get(`/search?${params}`, {})
    }
}
