import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMoneyCheck } from '@fortawesome/free-solid-svg-icons'
import { faAddressCard } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import App from './App.vue'
import router from './router'

library.add(faAddressCard)
library.add(faMoneyCheck)

const app = createApp(App)
app.component("font-awesome-icon", FontAwesomeIcon)
app.use(createPinia())
app.use(router)

app.mount('#app')
