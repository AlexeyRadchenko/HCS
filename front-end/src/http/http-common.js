import axios from 'axios';
import secureStorage from '../storage/secStorage'


const http = axios.create({})

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
  http.post('http://127.0.0.1:8030/api/v1/users_control_service/token', userFormData)
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
    setHeaders(http)
    return await http.get('http://localhost:8030/api/v1/users_control_service/management_users/me')
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

export var get_addresses_house_street_by_org_id = async function(id) {
    setHeaders(http)
    var api_url = `http://localhost:8050/api/v1/contacts_service/organisation/${id}/addresses_house_street`
    return await http.get(api_url)
    .then((response) => {
        if (response.status != 200)
          console.log(response.data, response.status)
        return response.data  
    })
    .catch(e => {
      if (!e.response) {
        console.log('сервер не отвечает')
      } else {
      }
    })
}

export var get_contacts_list = async function() {
  setHeaders(http)
  var api_url = `http://localhost:8050/api/v1/contacts_service/contacts_users/contacts`
  return await http.get(api_url)
  .then((response) => {
      if (response.status != 200)
        console.log(response.data, response.status)
      return response.data  
  })
  .catch(e => {
    if (!e.response) {
      console.log('сервер не отвечает')
    } else {
    }
  })
}

export var create_new_record_in_contacts = async function(formModalData) {
  setHeaders(http)
  var api_url = `http://localhost:8050/api/v1/contacts_service/contacts_users/create_contact`;
  return http.post(api_url, formModalData)
  .then((response) => {
      if (response.status != 200){
        console.log(response.data, response.status)
        return null
      }
      return response.data  
  })
  .catch(e => {
    if (!e.response) {
      console.log('сервер не отвечает')
      return null
    }
  })

}

export var update_record_in_contacts = async function(formModalData) {
  setHeaders(http)
  var api_url = `http://localhost:8050/api/v1/contacts_service/contacts_users/contact/` + formModalData.get('uuid');
  return http.put(api_url, formModalData)
  .then((response) => {
      if (response.status != 200){
        console.log(response.data, response.status)
        return null
      }
      return response.data  
  })
  .catch(e => {
    if (!e.response) {
      console.log('сервер не отвечает')
      return null
    }
  })
}

export var delete_record_in_contacts = async function(formModalData) {
  setHeaders(http)
  var api_url = `http://localhost:8050/api/v1/contacts_service/contacts_users/contact/` + formModalData.get('uuid');
  return http.delete(api_url, {data: {system_user: formModalData.get('system_user')}})
  .then((response) => {
      console.log(response.data, response.status)
      if (response.status != 200){
        console.log(response.data, response.status)
        return null
      }
      return response.data  
  })
  .catch(e => {
    if (!e.response) {
      console.log('сервер не отвечает')
      return null
    }
  })
}