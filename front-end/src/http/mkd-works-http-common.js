import axios from 'axios';
import secureStorage from '../storage/secStorage'

//console.log('ENV DATA', import.meta.env.VITE_API_BASEURL)
let api_main_url_port = import.meta.env.VITE_API_BASEURL;

if (import.meta.env.VITE_API_BASEPORT) {
  api_main_url_port = `${api_main_url_port}:${import.meta.env.VITE_API_BASEPORT}`;
}


const http = axios.create({})

var setHeaders = function (axios_instance) {

  var token = secureStorage.getItem('token')
  if (token)
    axios_instance.defaults.headers.common['Authorization'] = 'Bearer ' + token
  else
  axios_instance.defaults.headers.common['Authorization'] = null
  axios_instance.defaults.headers.common['Content-Type'] = 'application/json'

}

export var get_mkd_works_get_all_houses = async function () {
    setHeaders(http)
    return await http.get(api_main_url_port + '/api/v1/mkd_works_service/houses/all')
    .then(response => {
      if (response.status == 200)
        console.log(response)
        return response
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

export var get_mkd_works_get_all_works_by_house_id = async function (house_id) {
    setHeaders(http)
    return await http.get(api_main_url_port + '/api/v1/mkd_works_service/houses/works/all/' + house_id)
    .then(response => {
      if (response.status == 200)
        console.log(response)
        return response
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

export var get_future_work_id_by_house_id = async function (id) {
    setHeaders(http)
    return await http.get(api_main_url_port + '/api/v1/mkd_works_service/houses/works/future_id/' + id)
    .then(response => {
      if (response.status == 200)
        console.log(response)
        return response
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

export var get_works_reference_book = async function () {
    setHeaders(http)
    return await http.get(api_main_url_port + '/api/v1/mkd_works_service/get_reference_book_data/all')
    .then(response => {
      if (response.status == 200)
        console.log(response)
        return response
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


export var edit_mkd_works = async function (data) {
    setHeaders(http)
    return await http.post(api_main_url_port + '/api/v1/mkd_works_service/houses/works/edit/', data=data)
    .then(response => {
      if (response.status == 200)
        console.log(response)
        return response
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

export var create_new_mkd_works = async function (data) {
    setHeaders(http)
    return await http.post(api_main_url_port + '/api/v1/mkd_works_service/houses/works/create/', data=data)
    .then(response => {
      if (response.status == 200)
        console.log(response)
        return response
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

export var download_file_mkd_works = async function (url) {
    setHeaders(http)
    return await http.get(api_main_url_port + '/api/v1/mkd_works_service' + url, {responseType: 'blob'})
    .then(response => {
      if (response.status == 200)
        //console.log(response)
        return response
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

export var get_year_files_list_by_house = async function (house_id) {
    setHeaders(http)
    return await http.get(api_main_url_port + '/api/v1/mkd_works_service/houses/yearacts/all/' + house_id)
    .then(response => {
      if (response.status == 200)
        //console.log(response)
        return response
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

export var generate_year_file_by_house_and_year = async function (year, house_id) {
    setHeaders(http)
    return await http.get(api_main_url_port + '/api/v1/mkd_works_service/houses/yearacts/generate/' + year + '/' + house_id)
    .then(response => {
      if (response.status == 200)
        //console.log(response)
        return response
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
  
export var get_bg_task_status_by_task_uuid = async function (uuid) {
    setHeaders(http)
    return await http.get(api_main_url_port + '/api/v1/mkd_works_service/houses/yearacts/task/' + uuid +'/status')
    .then(response => {
      if (response.status == 200)
        //console.log(response)
        return response
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


export var get_year_act_file_by_uuid = async function (uuid) {
    setHeaders(http)
    return await http.get(api_main_url_port + '/api/v1/mkd_works_service/download/yearact/' + uuid, {responseType: 'blob'})
    .then(response => {
      if (response.status == 200)
        //console.log(response)
        return response
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

export var get_techdoc_files_list_by_house = async function (house_id) {
    setHeaders(http)
    return await http.get(api_main_url_port + '/api/v1/mkd_works_service/houses/techdocs/all/' + house_id)
    .then(response => {
      if (response.status == 200)
        //console.log(response)
        return response
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

export var request_director_data_drom_db = async function (house_id) {
  setHeaders(http)
  return await http.get(api_main_url_port + '/api/v1/mkd_works_service/house/' + house_id +'/director')
  .then(response => {
    if (response.status == 200)
      //console.log(response)
      return response
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

