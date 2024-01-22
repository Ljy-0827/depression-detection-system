import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router';
import ElementPlus from 'element-plus';
import zhCn from 'element-plus/es/locale/lang/zh-cn';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import "bootstrap-icons/font/bootstrap-icons.css";

import landingPage from '@/components/landingPage.vue';
import readingPage from "@/components/readingPage.vue";
import interviewPage from "@/components/interviewPage.vue";
import systemResultPage from "@/components/systemResultPage.vue";

const myRouter = createRouter({
    mode: 'history',
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [{
            path: '/',
            name: 'landing-page',
            component: landingPage,
        },
        {
            path: '/read',
            name: 'reading-page',
            component: readingPage,
        },
        {
            path: '/interview',
            name: 'interview-page',
            component: interviewPage,
        },
        {
            path: '/system_result',
            name: 'system-result-page',
            component: systemResultPage,
        }

    ]
})

const myApp = createApp(App)
myApp.use(myRouter)

myApp.mount('#app')

myApp.use(ElementPlus, {
    locale: zhCn,
})

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    myApp.component(key, component)
}