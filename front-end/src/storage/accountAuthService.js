import { defineStore } from 'pinia'
import secureStorage from './secStorage'

export const useAccountAuthStore = defineStore({
  id: 'AccountAuthStore',
  state: () => ({
    token: '',
    error: '',
    user: null,
    accountData: null,
    accountOrganisationData: null
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
    },
    getAccountData () {
      return this.accountData
    },
    getAccountOrganisationData () {
      return this.accountOrganisationData
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
    },
    setAccountData (data) {
      if (data) {
        this.accountData = data
      }
    },
    setAccountOrganisationData (data) {
      if (data) {
        this.accountOrganisationData = data
      }
    }
  }
})
