import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMoneyCheck, faAddressCard, faUserCheck, faBars, faAngleDown, faBook, faUser, faHouseUser, faRoad,
     faListOl, faBuilding, faWater, faQuestionCircle} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import 'element-plus/theme-chalk/display.css'
import VueTheMask from 'vue-the-mask'

import App from './App.vue'
import router from './router'
import { lib } from 'crypto-js'

library.add(faAddressCard)
library.add(faMoneyCheck)
library.add(faUserCheck)
library.add(faBars)
library.add(faAngleDown)
library.add(faBook)
library.add(faUser)
library.add(faHouseUser)
library.add(faRoad)
library.add(faBuilding)
library.add(faListOl)
library.add(faWater)
library.add(faQuestionCircle)

const app = createApp(App)
app.component("font-awesome-icon", FontAwesomeIcon)
app.use(createPinia())
app.use(router)
app.use(VueTheMask)

app.mount('#app')
