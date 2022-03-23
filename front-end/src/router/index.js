import { createRouter, createWebHistory } from 'vue-router'
import { current_active_user } from '../http/http-common'
import Authorisation from '../components/Authorisation.vue'
import Services from '../components/Services.vue'
import { useAuthStore } from '../storage/auth';
//import Contacts from '../components/Contacts.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'LoginPage',
      component: Authorisation
    },
    {
      path: '/services',
      name: 'services',
      component: Services
    },
    {
      path: '/management_accounts',
      name: 'contacts',
      //component: Contacts
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ContactsView.vue')
    }
  ]
})

const DEFAULT_TITLE = 'Komfort-Services';

router.beforeEach(async(to, from, next) => {
  document.title = to.meta.title || DEFAULT_TITLE;
  var authStore = useAuthStore()
  if (to.name !== 'LoginPage') {
    var user = await current_active_user()
    await authStore.setUser(user)
  }  
  if (to.name !== 'LoginPage' && !user) next({ name: 'LoginPage' })
  else next()
})

export default router
