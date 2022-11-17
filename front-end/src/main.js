import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import ru from 'element-plus/dist/locale/ru.mjs'
import { createPinia } from 'pinia'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMoneyCheck, faAddressCard, faUserCheck, faBars, faAngleDown, faBook, faUser, faHouseUser, faRoad,
     faListOl, faBuilding, faWater, faQuestionCircle, faFireAlt, faBolt} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import 'element-plus/theme-chalk/display.css'
import 'element-plus/dist/index.css'
import VueTheMask from 'vue-the-mask'

import App from './App.vue'
import router from './router'
import { lib } from 'crypto-js'

library.add(faAddressCard, faMoneyCheck, faUserCheck,
      faBars, faAngleDown, faBook, faUser, faHouseUser, 
      faRoad, faBuilding, faListOl, faWater, faQuestionCircle, faFireAlt,
      faBolt
      )

const app = createApp(App)
app.component("font-awesome-icon", FontAwesomeIcon)
app.use(ElementPlus, {locale: ru,})
app.use(createPinia())
app.use(router)
app.use(VueTheMask)

app.mount('#app')
