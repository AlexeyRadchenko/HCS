<template>
    <el-dialog v-model="dialogVisible" title="Загрузка данных об оплате" width="50%" draggable>
        <el-row>
            <el-col :span="12">
                <el-input v-model="inputPaymentFileName" placeholder="Выберите файл с данными по оплате"></el-input>
            </el-col>
            <el-col :span="4" :offset="1">
                <el-upload
                    ref="upload"
                    :limit="1"
                    :auto-upload="false"
                    :on-change="fileSelected"
                    :show-file-list="false"
                    >
                    <template #trigger>
                    <el-button type="primary">Выбрать файл</el-button>
                    </template>
                </el-upload>
            </el-col>
            <el-col :span="6">
                <el-button type="primary" @click.prevent="generatePaymentData">Сформировать данные</el-button>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="24">
                <el-alert
                    :title="msgErr"
                    type="error"
                    effect="dark"
                    id="il-payment_err"
                    v-if="showErr"
                 />
                <el-table :data="fileReadedData" style="width: 100%" max-height="500">
                    <el-table-column :formatter="dateFormatter" fixed prop="date" label="Дата" width="100" />
                    <el-table-column prop="type" label="Тип платежа" width="120" />
                    <el-table-column :formatter="paymentFormatter" prop="sum" label="Сумма" width="120" />
                    <el-table-column prop="il" label="Номер И/Л" width="120" />
                    <el-table-column prop="account_name" label="Плательщик" width="140" />
                    <el-table-column prop="company" label="Организация" width="240" />
                    <el-table-column fixed="right" label="Удалить" width="120">
                    <template #default="scope">
                        <el-button
                        link
                        type="primary"
                        size="small"
                        @click.prevent="deleteRow(scope.$index)"
                        >
                        Удалить
                        </el-button>
                    </template>
                    </el-table-column>
                </el-table>
                <el-form :inline="true" :model="formInline">
                    <el-row :gutter="10">
                        <el-col :span="4">
                            <el-date-picker
                                v-model="formInline.date"
                                type="date"
                                placeholder="Дата"
                                format="DD.MM.YYYY"
                                value-format="DD.MM.YYYY"
                                style="width: 100%;"
                                :clearable="false"
                            />
                        </el-col>
                        <el-col :span="4">
                            <el-select v-model="formInline.type" placeholder="Тип платежа">
                                <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                                />
                            </el-select>
                        </el-col>
                        <el-col :span="3">
                            <el-input v-model="formInline.sum" placeholder="Сумма" />
                        </el-col>
                        <el-col :span="3">    
                            <el-input v-model="formInline.il" placeholder="Номер И/Л" />
                        </el-col>
                        <el-col :span="6">    
                            <el-input v-model="formInline.account_name" placeholder="Плательщик" />
                        </el-col>
                        <el-col :span="4">    
                            <el-input v-model="formInline.company" placeholder="Организация" />
                        </el-col>    
                    </el-row>
                </el-form>
                <el-button class="mt-4" style="width: 100%" @click="onAddItem"
                    >Добавить строку</el-button
                >
            </el-col>
        </el-row>
        
        <template #footer>
        <span class="dialog-footer">
            <el-button @click="dialogVisible = false">Отмена</el-button>
            <el-button type="primary" @click.prevent="SendPaymentDataForUpload">
            Сохранить
            </el-button>
        </span>
        </template>
    </el-dialog>    
</template>

<script>
import secureStorage from '../../storage/secStorage'
import readXlsxFile from 'read-excel-file'
import { clearFilePaymentData, validate_payment_data } from '../../utils/utils'
import { debt_il_payment_data_upload } from '../../http/http-common'

export default {
  expose: ['dialogVisible', 'rowIdForDel'],
  setup() {
    let uploadHeaders = {
        'Authorization': 'Bearer ' + secureStorage.getItem('token')
    }
    const options = [
        {
            value: 'оплата по и/л',
            label: 'оплата по и/л'
        },
        {
            value: 'оплата касса и т.п.',
            label: 'оплата касса и т.п.'
        }
    ]
    return {
        uploadHeaders, options
    }
  },
  data() {
    return {
        dialogVisible: false,
        rowIdForDel: null,
        upload: null,
        inputPaymentFileName: '',
        inputFile: null,
        genDataReady: false,
        fileReadedData: [],
        formInline: {
            date: '',
            type: '',
            sum: '',
            il: '',
            account_name: '',
            company: '',
        },
        showErr: false,
        msgErr:''

    }
  },
  methods: {
    successUploadPaymentFile (response) {
        console.log(response)
    },
    fileSelected (uploadFile) {
        this.inputPaymentFileName = uploadFile.name
        this.inputFile = uploadFile.raw
    },
    generatePaymentData() {
        if (this.fileReadedData.length != 0){
            this.fileReadedData = []
        }
        readXlsxFile(this.inputFile).then((rows) => {
            let dataSlice = rows.slice(1)
            
            dataSlice.forEach(row => {
                clearFilePaymentData(row, this.fileReadedData)
            })
            console.log('Done')
        })
    },
    onAddItem () {
        let newRecord = {...this.formInline}
        this.fileReadedData.push(newRecord)
    },
    deleteRow (index) {
        this.fileReadedData.splice(index, 1)
    },
    paymentFormatter (row, column, cellValue, index) {
        return Number(cellValue).toFixed(2)       
    },
    dateFormatter (row, column, cellValue, index) {
        let regexp = /\d{2}.\d{2}.\d{4}/
        let date = cellValue.match(regexp)
        if (date) {
            return date[0]
        } else {
            return ''
        }
       
    },
    async SendPaymentDataForUpload() {
        let valid = await validate_payment_data (this.fileReadedData)
        this.msgErr = 'Все ячейки формы должны быть заполнены'
        //console.log(valid, this.fileReadedData)
        if (!valid) {
            this.showErr = true
        } else {
            this.showErr = false
            let response = await debt_il_payment_data_upload(this.fileReadedData)
            if (response.length !=0) {
                this.fileReadedData = response
                this.msgErr = 'Для записей не найден исполнительный лист, проверьте его наличие в базе и верный ли указан номер!'
                this.showErr = true
            } else {
                this.fileReadedData = []
                this.dialogVisible = false
            }
            
        }
    }
  }
}
</script>
<style scoped>
#il-payment_err {
    margin-top: 1em;
    margin-bottom: 1em;
}
</style>