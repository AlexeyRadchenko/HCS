import { stringify } from "uuid"

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
    contactData['work_phone'] = !fData['work_phones'] ? "" : fData['work_phones']
    contactData['mobile_phone'] = fData['mobile_phones']
    contactData['email'] = fData['emails']
    contactData['note'] = fData['note']
    return contactData
}

let getNamePayeerAndIL = (data_str) => {
    let il, name = null
    let regexp_il = /\d+\s?-\s?\d+\s?\/?\s?\d+/gm
    let il_reg = data_str.match(regexp_il)
    let il_reg_fullnum = data_str.match(/\d+/)
    let name_reg = data_str.match(/\D+/)
    //console.log(il_reg, name_reg, data_str)
    if (!il_reg && il_reg_fullnum){
        il = il_reg_fullnum[0].trim()
    }
    else {
        il = il_reg[0].trim()
    }
    if (!name_reg) {
        name = data_str
    }else {
        name = name_reg[0].trim()
    }
    //console.log('cllrrrrr', name, il)
    return { name, il }
}

let pushILDataToArr = (row, arrData, acc_name, il) => {
    arrData.push({
        date: row[0],
        type: 'квартплата по и/л' === row[3] ? 'оплата по и/л' : 'оплата касса и т.п.',
        sum: row[5],
        company: row[6],
        account_name: acc_name,
        il: il
    })
}

export let clearFilePaymentData = (row, accumData) => {
    let regexp_data = getNamePayeerAndIL(row[8])
    let acc_name = regexp_data.name
    let il = regexp_data.il
    if (accumData.length === 0) {
        pushILDataToArr(row, accumData, acc_name, il)
    }

    let find = false

    accumData.forEach(element => {
        if (element.il === il) {
            element.sum = (element.sum * 10 + row[5] * 10) / 10
            find = true
            return
        }
    })

    if (!find) {
        pushILDataToArr(row, accumData, acc_name, il)
    }
}

async function checkProperties(obj) {
    for (var key in obj) {
        if (obj[key] !== null && obj[key] != "")
            return false;
    }
    return true;
}

export let validate_payment_data = async (dataList) => {
    let status = true
    dataList.forEach (element => {
        for (var key in element) {
            if (element[key] === null || element[key] === '') {
                status = false
                return
            }        
        }
    })
    return status
}
export let mkd_works_works_to_string = function(main, sub, fix) {
    let works = ''
    for (let [index, element] of main.entries()) {works = works + element.work + '\n'}
    for (let [index, element] of sub.entries()) {works = works + element.work + '\n'}
    for (let [index, element] of fix.entries()) {works = works + element.work + '\n'}
    return works
}

export var get_mkd_works_sprav_name = function(main, sub, fix) {
    if (main.length > 0)
        return main[0].numsprav
    else if (sub.length > 0)
        return sub[0].numsprav
    else if (fix.length > 0)
        return fix[0].numsprav
    else return
}


export var get_period = function(sub, fix) {
    let mp = ''
    let sp = ''
    let fp = ''
    console.log("---------->",sub, fix)
    if (sub.length > 0)
        sp = sub[0].period
    if (fix.length > 0)
        fp = ' ' + fix[0].period
    console.log('-------', mp, sp, fp, mp + fp + sp )
    return mp + fp + sp
}

export var get_quantity_works = function (sub, fix) {
    
}

var getTypeWorkByName = function (nameW) {
    console.log('NAME SELECT TYEPE', nameW)
    let numType = nameW.split('_')[1]
    if (numType === '1') {
        return 'subwork'
    } else if (numType === '2') {
        return 'fixwork'
    } else if (parseInt(nameW) > 0) {
        return 'mainwork'
    }
    return
}

export var generate_data_object_to_post = function (workData, tableRowData, workID, houseID, periodOptions) {
    console.log("wokrID", workID)
    console.log("periodOptions", periodOptions)
    
    let postdata = {
        id: workID != '' ? workID : '-1',
        house_id: houseID,
        num: '',
        all_sum: workData.actAllSumHandle,
        directorSovietFIO: workData.directorSovietFIO,
        directorAppartNum: workData.directorAppartNum,
        all_sum: workData.actAllSumHandle,
        month_year_works: workData.workMonthAndYear,
        works: [],
        mainworks: workData.mainworks ? workData.mainworks.map(element => ({id: element.id, workType: element.workType})) : [],
        subworks: workData.subworks ? workData.subworks.map(element => ({id: element.id, workType: element.workType})) : [],
        fixworks: workData.fixworks ? workData.fixworks.map(element => ({id: element.id, workType: element.workType})) : [],
    }
    
    for (let [index, element] of tableRowData.entries()) {
        //console.log('POST ELEMENT', element.nameWorkOrService)
        postdata.num = element.numsprav
        console.log("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", element.workType, element.nameWorkOrService) 
        let typeWorkInput = element.nameWorkOrService.value ? element.nameWorkOrService.value : element.nameWorkOrService
        postdata.works.push({
            numsprav: element.numsprav,
            namework: element.nameWorkOrService.value ? element.nameWorkOrService.value : element.nameWorkOrService,
            period: typeof(element.period) === 'number' ? periodOptions[parseInt(element.period)].label : element.period,
            quantity: element.quantity,
            costofpart: element.costOfPart,
            sum: element.sum,
            workSubId: element.workSubId != '' ? element.workSubId : -1,
            workType: getTypeWorkByName(typeWorkInput),
            notes: element.notes,
        })
    }
    return postdata
}

export var clear_input_data = function (inputData, tableRowData, actInputData, smetaInputData) {
    inputData.value.workMonthAndYear = ''
    inputData.value.directorSovietFIO = ''
    inputData.value.directorAppartNum = ''
    inputData.value.actAllSumHandle = ''
    inputData.value.mainworks = []
    inputData.value.subworks= []
    inputData.value.fixworks = []
    tableRowData.value = [
        {
            orderNum: '1',
            nameWorkOrService: '',
            period: '',
            quantity: '',
            costOfPart: '',
            sum: '0.00',
            workType: '',
            workSubId: '',
            notes: '',
        }
    ]
    smetaInputData.value.smetanum = ''
    smetaInputData.value.smetadate = ''
    smetaInputData.value.actfutureid = ''
    smetaInputData.value.workid = ''
    smetaInputData.value.houseid = ''

    actInputData.value.actnum = ''
    actInputData.value.actdate = ''
    actInputData.value.actfutureid = ''
    actInputData.value.workid = ''
    actInputData.value.houseid = ''
}


/*export var get_work_value_by_label = function (label, data) {
    for (let [index, element] of data.entries()) {
        if (element.label === label)
            //console.log("2===========================", element.label, label)
            return {value: element.value, label:  element.label}
    }    
}*/

export var get_work_value_by_label = function (label, data) {
    // Функция для жесткой нормализации строки
    function normalizeText(text) {
        return text
            .trim() // Убираем пробелы в начале и конце
            .replace(/\s+/g, " ") // Заменяем все пробелы (включая неразрывные) на один обычный
            .replace(/\u00A0/g, " ") // Удаляем неразрывные пробелы
            .replace(/\u200B/g, "") // Убираем Zero-width space
            .replace(/\uFEFF/g, "") // Убираем BOM
            .normalize("NFC"); // Приводим к одной форме Юникода
    }

    const normalizedLabel = normalizeText(label);
    console.log("SEARCHING FOR:", JSON.stringify(normalizedLabel), JSON.stringify(normalizedLabel).length, data.length);

    for (let element of data) {
        const normalizedElementLabel = normalizeText(element.label);
        
        console.log("CHECKING:", JSON.stringify(normalizedElementLabel), JSON.stringify(normalizedElementLabel).length);
        
        if (normalizedElementLabel.substring(0,5) === normalizedLabel.substring(0,5)) {
            console.log("MATCH FOUND!");
            return { value: element.value, label: element.label };
        }
    }    

    console.log("NO MATCH FOUND!");
    return null;
};

export var get_mainwork_numspav = function (workname) {
    let result = workname.match(/^\s*(\d{1,2}\.)/);
    console.log('SEARCH RESULT:', result);
    return result ? result[1] : null; // Возвращаем число с точкой
}