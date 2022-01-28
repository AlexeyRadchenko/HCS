import { defineStore } from 'pinia'
import secureStorage from './secStorage'

export const useAuthStore = defineStore({
  id: 'AuthStore',
  state: () => ({
    token: '',
    error: ''
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
    }
  },
  actions: {
    setToken(token) {
      secureStorage.setItem('token', token)
      this.token = token
    },
    setError(error) {
      this.error = error
    }
  }
})
