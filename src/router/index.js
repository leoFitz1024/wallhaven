import { createRouter, createWebHashHistory } from "vue-router"

import onlineWall from '../views/online_wallpaper.vue'
import switchList from '../views/switch_list.vue'
import downlloadList from '../views/download_list.vue'
import setting from '../views/setting.vue'
import about from '../views/about_info.vue'
import preview from '../components/img_preview.vue'

const routes = [
    {
        path: '/',
        component: onlineWall          
    },
    {
        path: '/online',
        name: "online",
        component: onlineWall  
    },
    {
        path: '/switch',
        name: "switchList",
        component: switchList
    },
	{
	    path: '/download',
	    name: "downlloadList",
	    component: downlloadList
	},
	{
	    path: '/setting',
	    name: "setting",
	    component: setting
	},
	{
	    path: '/about',
	    name: "about",
	    component: about
	},
	{
	    path: '/preview',
	    name: "preview",
	    component: preview
	}
]
export const router = createRouter({
  history: createWebHashHistory(),
  routes: routes
})

export default router
