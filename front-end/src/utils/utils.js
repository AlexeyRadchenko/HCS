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
    if (ownerData == 'Владелец')
        return ownerData
    if (ownerData.full_owner)
        return 'Владелец'
    if (ownerData.part_owner)
        return ownerData.part_size
}

export var getModalFormObject = function (formModalData) {
    if (formModalData.part_own == 'Владелец')
        formModalData.part_own = '1'
    var formData = new FormData ()
    for (const [key, value] of Object.entries(formModalData)) {
        formData.append(`${key}`, `${value}`)
    }
    return formData
       
}

export var serverDataToTableRows = async function (srcLs) {
    var resultTableStr = []
    srcLs.forEach(function (srcElement) {
        var contactData = {}
        srcElement.addresses.forEach(function (addressElement) {
                contactData['uuid'] = srcElement.uuid
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

export var ContactDataObjectToTableObject = async function (fData) {
    var contactData = {}
    contactData['uuid'] = fData['uuid']
    contactData['house'] = fData['street_house'].split('_')[0]
    contactData['entrance'] = fData['entrance']
    contactData['appartment'] = fData['appartment']
    contactData['FIO'] = fData['name'] + ' ' + fData['second_name'] + ' ' + fData['surname']
    contactData['part_have'] = (fData['part_own'] == '1') ? 'Владелец' : fData['part_own']
    contactData['home_phone'] = fData['home_phones']
    contactData['work_phone'] = fData['work_phones']
    contactData['mobile_phone'] = fData['mobile_phones']
    contactData['email'] = fData['emails']
    contactData['note'] = fData['note']
    return contactData
}
