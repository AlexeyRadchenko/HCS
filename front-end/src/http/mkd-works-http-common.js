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

export var get_mkd_works_all_data = async function () {
    setHeaders(http)
    return await http.get('http://localhost:8050/api/v1/mkd_works_service/data/all')
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