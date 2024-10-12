import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import { createPinia } from 'pinia'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMoneyCheck, faAddressCard, faUserCheck, faBars, faAngleDown, faBook, faUser, faHouseUser, faRoad,
     faListOl, faBuilding, faWater, faQuestionCircle, faFireAlt, faBolt, faHouse} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import 'element-plus/theme-chalk/display.css'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import VueTheMask from 'vue-the-mask'
import ru from 'element-plus/es/locale/lang/ru'
import 'dayjs/locale/ru'

import App from './App.vue'
import router from './router'
import { lib } from 'crypto-js'
import { locale } from 'dayjs'

library.add(faAddressCard, faMoneyCheck, faUserCheck,
      faBars, faAngleDown, faBook, faUser, faHouseUser, 
      faRoad, faBuilding, faListOl, faWater, faQuestionCircle, faFireAlt,
      faBolt, faHouse
      )

const app = createApp(App)
app.component("font-awesome-icon", FontAwesomeIcon)
app.use(ElementPlus, {locale: ru,})
app.use(createPinia())
app.use(router)
app.use(VueTheMask)

app.mount('#app')
