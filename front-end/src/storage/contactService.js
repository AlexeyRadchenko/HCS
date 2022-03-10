import { defineStore } from 'pinia'

export const useContactStore = defineStore({
    id: 'ContactsServiceStore',
    state: () => ({
      error: '',
      contactsServiceTableData: [],
      hasChanged: false
    }),
    getters: {
      getError () {
        return this.error
      },
      getContactsServiceTableData () {
        return this.contactsServiceTableData
      },
      changedState() {
        return this.hasChanged
      }
    },
    actions: {
      setError(error) {
        this.error = error
      },
      setContactsServiceTableData (data) {
        this.contactsServiceTableData = data
        this.hasChanged = true
      },
      addContactsServiceTableDataRow (row) {
        this.contactsServiceTableData.push(row)
        this.hasChanged = true
      },
      setStateStatus(status) {
          this.hasChanged = status
      }
    }
  })
  