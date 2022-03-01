export var handleAddresses = async function(adresses) {
    var resultArr = []
    adresses.reverse().forEach(element => {
      resultArr.push(element.street + ' - ' + element.house_number)
    })
    return resultArr
  }

export var handleModalAddresses = function (addresses) {
    var result_list = []
    addresses.forEach(element => {
        result_list.push({
            value: element.street + ' - ' + element.house_number + '_' + element.organisation_id,
            label: element.street + ' - ' + element.house_number
        })
    })
    return result_list
}  

var getOwner = function (ownerData) {
    if (ownerData.full_owner)
        return 'Владелец'
    if (ownerData.part_owner)
        return ownerData.part_size
}

export var serverDataToTableRows = async function (srcLs) {
    var resultTableStr = []
    srcLs.forEach(function (srcElement) {
        var contactData = {}
        srcElement.addresses.forEach(function (addressElement) {
                contactData['house'] = addressElement.address_data.street + ' - ' + addressElement.address_data.house_number
                contactData['entrance'] = addressElement.address_data.entrance
                contactData['appartment'] = addressElement.address_data.appartment
                contactData['FIO'] = srcElement.name + ' ' + srcElement.second_name + ' ' + srcElement.surname
                contactData['part_have'] = getOwner(addressElement)
                contactData['home_phone'] = !srcElement.phones.length ? "" : srcElement.phones[0].home_phone
                contactData['work_phone'] = !srcElement.phones.length ? "" : srcElement.phones[0].work_phone
                contactData['mobile_phone'] = !srcElement.phones.length ? "" : srcElement.phones[0].mobile_phone
                contactData['email'] = !srcElement.emails.length ? "" : srcElement.emails[0].email
                contactData['note'] = srcElement.note
                resultTableStr.push(contactData)
        })
    })
    return resultTableStr
}