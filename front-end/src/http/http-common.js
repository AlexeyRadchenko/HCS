import axios from 'axios';
import secureStorage from '../storage/secStorage'


const http = axios.create({
  baseURL: 'http://localhost:8000'
})

var setHeaders = function (axios_instance) {
  var token = secureStorage.getItem('token')
  if (token)
    axios_instance.defaults.headers.common['Authorization'] = 'Bearer ' + token
  else
  axios_instance.defaults.headers.common['Authorization'] = null
  axios_instance.defaults.headers.common['Content-Type'] = 'application/json'
} 

export var login = function(authStore, userFormData, loading, router) {
  var token = null
  http.post('/users_control_service/token', userFormData)
    .then(response => {
      if (response.status == 200)
        token = response.data.access_token
        authStore.setToken(token)
        router.push('services')
        loading.close()
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

export var current_active_user = async function () {
    console.log('storage', secureStorage.getItem('token'))
    setHeaders(http)
    return await http.get('users_control_service/management_users/me')
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


