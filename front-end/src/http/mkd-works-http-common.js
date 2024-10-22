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

export var get_mkd_works_get_all_houses = async function () {
    setHeaders(http)
    return await http.get('http://localhost:8050/api/v1/mkd_works_service/houses/all')
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
    return await http.get('http://localhost:8050/api/v1/mkd_works_service/houses/works/future_id/' + id)
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
