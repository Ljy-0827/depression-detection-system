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
import waitingResultPage from "@/components/waitingResultPage.vue";
import questionnairePage from "@/components/questionnairePage.vue";
import questionnaireResultPage from "@/components/questionnaireResultPage.vue";
import landingPageWide from "@/components/landingPageWide.vue";
import readingPageWide from "@/components/readingPageWide.vue";
import interviewPageWide from "@/components/interviewPageWide.vue";
import systemResultPageWide from "@/components/systemResultPageWide.vue";
import questionnairePageWide from "@/components/questionnairePageWide.vue";
import questionnaireResultPageWide from "@/components/questionnaireResultPageWide.vue";
import waitingResultPageWide from "@/components/waitingResultPageWide.vue";

const myRouter = createRouter({
    mode: 'history',
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [{
            path: '/wide',
            name: 'landing-page',
            component: landingPage,
        },
        {
          path: '/',
          name: 'landing-page-wide',
          component: landingPageWide,
        },
        {
            path: '/read',
            name: 'reading-page',
            component: readingPage,
        },
        {
            path: '/read_wide',
            name: 'reading-page-wide',
            component: readingPageWide,
        },
        {
            path: '/interview',
            name: 'interview-page',
            component: interviewPage,
        },
        {
            path: '/interview_wide',
            name: 'interview-page-wide',
            component: interviewPageWide,
        },
        {
            path: '/waiting',
            name: 'waiting-result-page',
            component: waitingResultPage,
        },
        {
            path: '/waiting_wide',
            name: 'waiting-result-page-wide',
            component: waitingResultPageWide,
        },
        {
            path: '/system_result',
            name: 'system-result-page',
            component: systemResultPage,
        },
        {
            path: '/system_result_wide',
            name: 'system-result-page-wide',
            component: systemResultPageWide,
        },
        {
            path: '/questionnaire',
            name: 'questionnaire-page',
            component: questionnairePage,
        },
        {
            path: '/questionnaire_wide',
            name: 'questionnaire-page-wide',
            component: questionnairePageWide,
        },
        {
            path: '/questionnaire_result',
            name: 'questionnaire-result-page',
            component: questionnaireResultPage,
        },
        {
            path: '/questionnaire_result_wide',
            name: 'questionnaire-result-page-wide',
            component: questionnaireResultPageWide,
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