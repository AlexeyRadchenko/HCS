import { defineStore } from 'pinia'
import secureStorage from './secStorage'

export const useAuthStore = defineStore({
  id: 'AuthStore',
  state: () => ({
    token: '',
    error: '',
    user: null
  }),
  getters: {
    getToken () {
      if (this.token)
        return this.token
      else
        return secureStorage.getItem('token')
    },
    getError () {
      return this.error
    },
    getUser() {
      if (this.user)
        return this.user
      else
        return secureStorage.getItem('user')
    }
  },
  actions: {
    setToken(token) {
      secureStorage.setItem('token', token)
      this.token = token
    },
    setError(error) {
      this.error = error
    },
    async setUser(user) {
      if (user) {
        secureStorage.setItem('user', user)
        this.user = user
      }
    }
  }
})
