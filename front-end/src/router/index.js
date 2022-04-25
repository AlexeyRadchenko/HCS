import { createRouter, createWebHistory } from 'vue-router'
import { current_active_user } from '../http/http-common'
import { current_active_acc_user } from '../http/account-http-common'
import Authorisation from '../components/Authorisation.vue'
import Services from '../components/Services.vue'
import { useAuthStore } from '../storage/auth';
import { useAccountAuthStore } from '../storage/accountAuthService';
import ClientsAuthorisation from '../components/ClientsAuthorisation.vue'

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
      name: 'Services',
      component: Services
    },
    {
      path: '/management_accounts',
      name: 'Contacts',
      //component: Contacts
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ContactsView.vue')
    },
    {
      path: '/accounts/login',
      name: 'ClientsLogin',
      component: ClientsAuthorisation
    },
    {
      path: '/accounts/:account',
      name: 'AccountDashBoard',
      component: () => import('../views/AccountDashBoardView.vue')
    },
  ]
})

const DEFAULT_TITLE = 'Komfort-Services';

router.beforeEach(async(to, from, next) => {
  document.title = to.meta.title || DEFAULT_TITLE;
  var authStore = useAuthStore()
  var accAuthStore = useAccountAuthStore()
  if (to.name !== 'LoginPage' && !to.path.includes('/accounts/')) {
    var user = await current_active_user()
    await authStore.setUser(user)
  }  
  if (to.name !== 'ClientsLogin' && to.path.includes('/accounts/')) {
    var accUser = await current_active_acc_user()
    await accAuthStore.setUser(accUser)
  } 
  if (to.name !== 'ClientsLogin' && to.path.includes('/accounts/') && !accUser ) next({ name: 'ClientsLogin' })
  if (to.name !== 'LoginPage' && !to.path.includes('/accounts/') && !user) next({ name: 'LoginPage' })
  else next()
})

export default router
