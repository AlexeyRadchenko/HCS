import axios from 'axios';
import secureStorage from '../storage/secStorage'


const http = axios.create({})

var setHeaders = function (axios_instance) {

  var token = secureStorage.getItem('AccToken')
  if (token)
    axios_instance.defaults.headers.common['Authorization'] = 'Bearer ' + token
  else
  axios_instance.defaults.headers.common['Authorization'] = null
  axios_instance.defaults.headers.common['Content-Type'] = 'application/json'

} 

export var accountLogin = function(authStore, userFormData, loading, router) {
  var token = null
  http.post('http://127.0.0.1:8030/api/v1/users_control_service/account_token', userFormData)
    .then(response => {
      if (response.status == 200) {
        console.log(response.data)
        token = response.data.access_token
        authStore.setToken(token)
        router.push({ name: 'AccountDashBoard', params: { account: userFormData.get('username')} })
        loading.close()
      }
    })
    .catch(e => {
        if (!e.response) {
          authStore.setError('Сервер не отвечает')
          loading.close()
        }
        else if (e.response.status == 401) {
          authStore.setError('Неправильно указан пользователь или пароль')
          loading.close()
        }  
        else if (e.response.status == 422) {
          authStore.setError('Введите имя пользователя и пароль')
          loading.close()
        }        
    })
  }

export var current_active_acc_user = async function () {
    setHeaders(http)
    return await http.get('http://localhost:8030/api/v1/users_control_service/account/me')
    .then(response => {
      if (response.status == 200)
        return response.data
    })
    .catch(e => {
      if (!e.response) {
        console.log('сервер не отвечает')
        return null
      } else {
        return null
      }
    })
  }

export var get_account_data_by_acc = async function (account) {
  setHeaders(http)
  return await http.get('http://localhost:8070/api/v1/accounts_service/account/' + account + '/data')
  .then(response => {
    if (response.status == 200)
      return response.data
  })
  .catch(e => {
    if (!e.response) {
      console.log('сервер не отвечает')
      return null
    } else {
      return null
    }
  })
}

export var put_counter_data_by_counter_id = async function(counterFormData, account) {
  setHeaders(http)
  return await http.put('http://localhost:8070/api/v1/accounts_service/account/' + account + '/update_water_counter_data', counterFormData)
  .then(response => {
    if (response.status == 200){
      return response.data
    }  
  })
  .catch(e => {
    if (!e.response) {
      console.log('сервер не отвечает')
      return null
    } else {
      return null
    }
  })
}

