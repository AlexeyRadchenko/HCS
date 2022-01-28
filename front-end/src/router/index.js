import { createRouter, createWebHistory } from 'vue-router'
import { current_active_user } from '../http/http-common'
import Authorisation from '../components/Authorisation.vue'
import Services from '../components/Services.vue'
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

router.beforeEach(async(to, from, next) => {
  console.log(to.name, from.name)
  if (to.name !== 'LoginPage')
    var user = await current_active_user()
    //var userd = user.then((response) => response.data)
  if (to.name !== 'LoginPage' && !user) next({ name: 'LoginPage' })
  else next()
})

export default router
