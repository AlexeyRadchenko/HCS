import { defineStore } from 'pinia'
import secureStorage from './secStorage'

export const useAccountAuthStore = defineStore({
  id: 'AccountAuthStore',
  state: () => ({
    token: '',
    error: '',
    user: null,
  }),
  getters: {
    getToken () {
      if (this.token)
        return this.token
      else
        return secureStorage.getItem('AccToken')
    },
    getError () {
      return this.error
    },
    getUser() {
      if (this.user)
        return this.user
      else
        return secureStorage.getItem('AccUser')
    }
  },
  actions: {
    setToken(token) {
      secureStorage.setItem('AccToken', token)
      this.token = token
    },
    setError(error) {
      this.error = error
    },
    flushTokenUser () {
      secureStorage.setItem('AccUser', '')
      secureStorage.setItem('AccToken', '')
      this.token = ''
      this.user = null
    },
    async setUser(user) {
      if (user) {
        secureStorage.setItem('AccUser', user)
        this.user = user
      }
    }
  }
})
