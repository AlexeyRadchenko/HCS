import axios from 'axios';
import secureStorage from '../storage/secStorage'
import fileDownload from 'js-file-download'

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
  http.post(import.meta.env.VITE_API_USER_CONTROL_ROOT+'/api/v1/users_control_service/token', userFormData)
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
    return await http.get(import.meta.env.VITE_API_USER_CONTROL_ROOT+'/api/v1/users_control_service/management_users/me')
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
    var api_url = import.meta.env.VITE_API_CONTACTS_ROOT+`/api/v1/contacts_service/organisation/${id}/addresses_house_street`
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
  var api_url = import.meta.env.VITE_API_CONTACTS_ROOT+`/api/v1/contacts_service/contacts_users/contacts`
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
  var api_url = import.meta.env.VITE_API_CONTACTS_ROOT+`/api/v1/contacts_service/contacts_users/create_contact`;
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
  var api_url = import.meta.env.VITE_API_CONTACTS_ROOT+`/api/v1/contacts_service/contacts_users/contact/` + formModalData.get('uuid');
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
  var api_url = import.meta.env.VITE_API_CONTACTS_ROOT+`/api/v1/contacts_service/contacts_users/contact/` + formModalData.get('uuid');
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

export var debt_il_get_all_il_list = async function () {
  setHeaders(http)
  return await http.get(import.meta.env.VITE_API_DEBT_IL_ROOT+'/api/v1/debt_il_service/il/all/data')
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

export var debt_il_get_all_il_list_by_edge_date = async function (monthYear) {
  setHeaders(http)
  return await http.get(import.meta.env.VITE_API_DEBT_IL_ROOT+'/api/v1/debt_il_service/il/' + monthYear + '/data')
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

export var debt_il_get_all_accounts_il_list = async function () {
  setHeaders(http)
  return await http.get(import.meta.env.VITE_API_DEBT_IL_ROOT+'/api/v1/debt_il_service/il/accounts/all/data')
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


export var debt_il_get_egrn_docs_by_id_il = async function (il_id) {
  setHeaders(http)
  return await http.get(import.meta.env.VITE_API_DEBT_IL_ROOT+'/api/v1/debt_il_service/il/egrn_il_doc/data/' + il_id)
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

export var debt_il_del_egrn_docs_by_egrn_doc_id = async function (egrn_doc_id) {
  setHeaders(http)
  return await http.delete(import.meta.env.VITE_API_DEBT_IL_ROOT+'/api/v1/debt_il_service/il/egrn_il_doc/data/' + egrn_doc_id)
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


export var debt_il_download_egrn_docs_by_file_path = async function (file_path, file_name) {
  setHeaders(http)
  let data = { file_name: file_name, file_path: file_path }
  return await http.post(import.meta.env.VITE_API_DEBT_IL_ROOT+'/api/v1/debt_il_service/il/egrn_il_doc/download/', data, {responseType: 'blob' })
  .then(response => {
    if (response.status == 200)
      {
        fileDownload(response.data, file_name);
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

export var debt_il_payment_data_upload = async function (data_list) {
  setHeaders(http)
  return await http.post(import.meta.env.VITE_API_DEBT_IL_ROOT+'/api/v1/debt_il_service/il/payment_il_doc/data/upload', { data: data_list })
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

export var debt_il_get_payments_il_by_id_il = async function (il_id) {
  setHeaders(http)
  return await http.get(import.meta.env.VITE_API_DEBT_IL_ROOT+'/api/v1/debt_il_service/il/payments_il_doc/data/' + il_id)
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