<template>
<div class="debt-il-wrapper-conteiner">
  <el-container >
    <el-header height="120px">
      <el-row>
        <el-col :span="8"><div class="service-title"><h1>{{ serviceTitle }}</h1></div></el-col>  
        <el-col :span="12"><div></div></el-col>
        <el-col :span="4"></el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="3" class="filters-row-column">
          <el-input v-model="searchAddress" placeholder="Адрес"></el-input>
        </el-col>
        <el-col :span="4" class="filters-row-column">
          <el-input v-model="searchFIO" placeholder="ФИО"></el-input>
        </el-col>
        <el-col :span="3" class="filters-row-column">
          <el-input v-model="searchIL" placeholder="Номер и/л"></el-input>
        </el-col>
        <el-col :span="6" class="filters-row-column">
        
        </el-col>
        <el-col :span="8" class="main-button-row-column">
          <el-button type="primary">Сформировать отчет</el-button>
          <el-button type="primary" @click="this.$refs.paymentsUploadDialog.dialogVisible = true">Загрузить сведения об оплате</el-button>
          <el-button type="primary" @click="this.$refs.createRecordDialog.dialogVisible = true">Добавить запись</el-button>
        </el-col>  
      </el-row>    
    </el-header>
    <el-main>
      <el-row>
        <el-col :span="24">
            <el-skeleton :rows="10" animated v-if="!showTable" />
            <el-table :data="filterTableData"  row-key="id" style="width: 100%" max-height="55em" v-if="showTable">
              <el-table-column label="Адрес" width="180" :formatter="addressTableFormatter" sortable :sort-method="addressSort" align="center" />
              <el-table-column label="Собственность" width="145" align="center" :formatter="OneOrPartsOwnFormatter" />
              <el-table-column align="center" :formatter="typeOwnFormatter" label="Част./Соц. найм" width="150" />
              <el-table-column prop="il_number" label="№ исполнительного производства"  width="120" align="center"/>
              <el-table-column type="expand">
                <template #default="props">
                  <div class="debt-sub-table">
                    <el-row>
                      <el-col :span="6">
                      <h2><span>Адрес:</span> {{ props.row.street }} {{ props.row.house }} - {{ props.row.appartment }} </h2>
                      </el-col>
                      <el-col :span="8">
                        <el-button @click="egrnDocDialogCall(props.row.id, props.row.il_number)">Сведения ЕГРН</el-button>
                        <el-button>Судбный приказ</el-button>
                        <el-button>Отменненный судбный приказ</el-button>
                        <el-button @click="paymentHistoryDialogCall(props.row.id, props.row.il_number)">История платежей</el-button>
                      </el-col>
                      <el-col :span="10">
                       
                      </el-col> 
                    </el-row>
                    <h2>Физ. лица</h2>
                    <el-table :data="props.row.accounts_il">
                      <el-table-column label="Лицевой счет" prop="account_number" width="115" align="center" />
                      <el-table-column label="ФИО" :formatter="fioFormatter" align="center" width="450" />
                      <el-table-column label="Дата рождения" :formatter="dateCellFormatter" prop="passport_il.birth_date" align="center"  width="115" />
                      <el-table-column label="Место рождения" prop="passport_il.birth_place" align="center" width="120" />
                      <el-table-column label="Серия и номер паспорта" :formatter="passportFormatter" align="center" width="120" />
                      <el-table-column label="Кем и когда выдан" :formatter="passportWhoAndWhereFormatter" align="center"  width="430" />
                      <el-table-column label="Код подразделения" prop="passport_il.squad_code" align="center" width="110" />
                      <el-table-column label="Скан паспорта" prop="passport_il.scan" align="center" width="110" />
                    </el-table>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="Физ. Лица" align="center" width="250">
                <template #default="scope">
                  <ul style="list-style-type: none;">
                    <li v-for="item in scope.row.accounts_il" :key="item.uuid">{{ item.surname }} {{ item.name }} {{ item.second_name }}</li>
                  </ul>
                </template>
              </el-table-column>  
              <el-table-column prop="start_exec_pross_date" :formatter="dateCellFormatter" label="Дата исп./произиводства" width="120" align="center" />
              <el-table-column prop="gov_tax" :formatter="decimalCellFormatter" label="Сумма госпошлины" width="120" align="center" />
              <el-table-column prop="debt_sum" :formatter="decimalCellFormatter" label="Сумма долга" width="120" align="center" />
              <el-table-column prop="sum_all_get" :formatter="decimalCellFormatter" label="Взысканная сумма" width="120" align="center" />
              <el-table-column prop="sum_not_yet_get" :formatter="decimalCellFormatter" label="Остаток задолженности" width="120" />
              <el-table-column label="Передано юристу" width="130" align="center">
                <template #default="scope">
                      <el-checkbox v-model="scope.row.ur_in_work" :label="scope.row.ur_in_work ? 'В работе' : 'Передать'" size="large" border />
                </template>
              </el-table-column>  
              <el-table-column prop="period" label="Период задолженности" width="120" />
              <el-table-column label="Дата окончания произодства" width="120" />
              <el-table-column label="Причина окончания произодства" width="120" />
              <el-table-column label="Был отменен" width="100" align="center" :filters="[
                { text: 'Да', value: 'Да' },
                { text: 'Нет', value: 'Нет' },
              ]"
              :filter-method="filterOrderCancel">
                <template #default="scope">
                  <span v-if="scope.row.order_cancel">Да</span>
                  <span v-else>Нет</span>
                </template>
              </el-table-column>  
              <el-table-column label="Примечание" width="120" />
              <el-table-column fixed="right" label="Редактирование" width="240" align="center">
                <template #default="scope">
                  <el-button
                    type="primary"
                    @click.prevent="changeRow(scope.$index)"
                   >Изменить</el-button>
                  <el-button
                  @click.prevent="deleteRow(scope.$index)"
                  type="danger"
                  >Удалить</el-button>
                </template>
              </el-table-column>
            </el-table>  
        </el-col>  
      </el-row>  
    </el-main>  
  </el-container>
  <CreateRecordDialog ref="createRecordDialog" />
  <UpdateRecordDialog ref="updateRecordDialog" />
  <DeleteRecordDialog ref="deleteRecordDialog" />
  <EGRNDocsDialog ref="egrnDocsDialog" />
  <PaymentsUploadDialog ref="paymentsUploadDialog" />
  <PaymentsHistoryDialog ref="paymentsHistoryDialog" />
</div>  
</template>

<script>
import moment from 'moment/dist/moment'
import ru from 'moment/dist/locale/ru'
import { debt_il_get_all_il_list } from '../../http/http-common'
import CreateRecordDialog from './CreateRecordDialog.vue'
import UpdateRecordDialog from './UpdateRecordDialog.vue'
import DeleteRecordDialog from './DeleteRecordDialog.vue'
import EGRNDocsDialog from './EGRNDocsDialog.vue'
import PaymentsUploadDialog from './PaymentsUploadDialog.vue'
import PaymentsHistoryDialog from './PaymentsHistoryDialog.vue'

export default {
  components: {
    CreateRecordDialog,
    UpdateRecordDialog,
    DeleteRecordDialog,
    EGRNDocsDialog,
    PaymentsUploadDialog,
    PaymentsHistoryDialog,
  },
  setup() {
    moment.updateLocale('ru', ru)
    return { moment }
  },
  data() {
    return {
        serviceTitle: 'Задолженность по испольнительным листам',
        searchAddress: '',
        searchFIO: '',
        searchIL: '',
        /*tableData: [
          {
            id: 0,
            street: "60 лет Октября",
            house: "10",
            appartment: "20",
            accounts_il: [
              {
                uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                account_number: "100002222",
                name: "Иван",
                second_name: "Иванович",
                surname: "Иванов",
                passport_il: {
                  id: 0,
                  seria: "74 05",
                  number: "111111",
                  who_take: "ОВД администрации города Трехгорного Челябинской области",
                  when_take: "2022-11-02T10:56:04.116Z",
                  squad_code: "740-000",
                  birth_date: "2022-11-02T10:56:04.116Z",
                  birth_place: "г Златоуст-36 Челябинской области",
                  scan: "string"
                }
              },
              {
                uuid: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                account_number: "100002222",
                name: "Петр",
                second_name: "Петрович",
                surname: "Петров",
                passport_il: {
                  id: 0,
                  seria: "75 05",
                  number: "0000000",
                  who_take: "ОВД администрации города Трехгорного Челябинской области",
                  when_take: "2022-11-02T10:56:04.116Z",
                  squad_code: "740-000",
                  birth_date: "2022-11-02T10:56:04.116Z",
                  birth_place: "г Златоуст-36 Челябинской области",
                  scan: "string"
                }
              }
            ],
            "egrn_il": [
              {
                "id": 0,
                "date": "2022-11-10T09:20:55.717Z",
                "number": "string",
                "file": "string"
              }
            ],
            property_self: true,
            one_or_parts: true,
            il_number: "2-445/2022",
            il_date: "2022-11-02T10:56:04.116Z",
            ur_in_work: true,
            gov_tax: 1000.45,
            order_cancel: true,
            bailiff_forward_date: "2022-11-02T10:56:04.116Z",
            start_exec_pross_date: "2022-11-02T10:56:04.116Z",
            end_exec_pross_date: "2022-11-02T10:56:04.116Z",
            period:[],
            sum_all_get: 50000.00,
            sum_not_yet_get: 255000.70,
            payments: 0,
            payments_il: [
              {
                id: 0,
                date: "2022-11-02T10:56:04.116Z",
                type: "string",
                sum: 0
              }
            ],
            debt_sum: 305156.54,
            notes: "string"
          },
          
          {
            id: 1,
            street: "50 лет победы",
            house: "10",
            appartment: "20",
            accounts_il: [
              {
                uuid: "3fa85f64-5717-4562-b3fc-2b963f66afa6",
                account_number: "100002222",
                name: "Иван",
                second_name: "Иванович",
                surname: "Иванов",
                passport_il: {
                  id: 1,
                  seria: "74 05",
                  number: "111111",
                  who_take: "ОВД администрации города Трехгорного Челябинской области",
                  when_take: "2022-11-02T10:56:04.116Z",
                  squad_code: "740-000",
                  birth_date: "2022-11-02T10:56:04.116Z",
                  birth_place: "г Златоуст-36 Челябинской области",
                  scan: "string"
                }
              },
              {
                uuid: "3fa85f64-5717-4562-b3fc-2c983f66afa6",
                account_number: "100002222",
                name: "Петр",
                second_name: "Петрович",
                surname: "Петров",
                passport_il: {
                  id: 2,
                  seria: "75 05",
                  number: "0000000",
                  who_take: "ОВД администрации города Трехгорного Челябинской области",
                  when_take: "2022-11-02T10:56:04.116Z",
                  squad_code: "740-000",
                  birth_date: "2022-11-02T10:56:04.116Z",
                  birth_place: "г Златоуст-36 Челябинской области",
                  scan: "string"
                }
              }
            ],
            "egrn_il": [
              {
                "id": 0,
                "date": "2022-11-10T09:20:55.717Z",
                "number": "string",
                "file": "string"
              }
            ],
            property_self: true,
            one_or_parts: true,
            il_number: "2-446/2022",
            il_date: "2022-11-02T10:56:04.116Z",
            ur_in_work: true,
            gov_tax: 1000.45,
            order_cancel: false,
            bailiff_forward_date: "2022-11-02T10:56:04.116Z",
            start_exec_pross_date: "2022-11-02T10:56:04.116Z",
            end_exec_pross_date: "2022-10-02T10:56:04.116Z",
            period:[],
            sum_all_get: 50000.00,
            sum_not_yet_get: 255000.70,
            payments: 0,
            payments_il: [
              {
                id: 0,
                date: "2022-11-02T10:56:04.116Z",
                type: "string",
                sum: 0
              }
            ],
            debt_sum: 305156.54,
            notes: "string"
          }
       ],*/
        tableData:[],
        showTable:false,   
    }
  },
  methods: {
    addressTableFormatter (row, column) {
      return row.street + ' ' + row.house + ' - ' + row.appartment
    },
    typeOwnFormatter (row, column) {
      if (row.property_self)
        return 'Частная'
      return 'Соц. найм'
    },
    OneOrPartsOwnFormatter (row, column) {
      if (row.one_or_parts)
        return 'Один собственник'
      return 'Долевая'
    },
    fioFormatter (row, column) {
      return row.surname + ' ' + row.name + ' ' + row.second_name
    },
    passportFormatter (row, column) {
      return row.passport_il.serial + ' ' + row.passport_il.number
    },
    passportWhoAndWhereFormatter (row, column) {
      let where = moment(row.passport_il.when_take).format('L')
      return row.passport_il.who_take + ' ' + where
    },
    dateCellFormatter (row, column, cellValue) {
      return moment(cellValue).format('L')
    },
    decimalCellFormatter (row, column, cellValue) {
      return Number(cellValue).toFixed(2);
    },
    LawerButtonstatus (value) {
      if (value)
        return 'В работе'
      else
        return 'Передать'
    },
    addressSort (a, b) {
      let adr1 = a.street + ' ' + a.house + ' - ' + a.appartment
      let adr2 = b.street + ' ' + b.house + ' - ' + b.appartment
      let sortded = [adr1, adr2].sort()
      if (sortded[0] === adr1)
        return 0
      return 1
    }, 
    filterOrderCancel (value, row) {
      let orderTypeMap = {'Да': true, 'Нет': false}
      return row.order_cancel === orderTypeMap[value]
    },
    changeRow(rowIndex) {
      this.filterTableData[rowIndex].accounts_il.forEach(element => {
        if (!element.passport_il) {
          element.passport_il = {
            id: element.id,
            serial: "",
            number: "",
            who_take: "",
            when_take: "",
            squad_code: "",
            birth_date: "",
            birth_place: "",
            scan: ""
          }
        }
      })
    
      this.$refs.updateRecordDialog.dialogVisible = true
      this.$refs.updateRecordDialog.ruleForm = this.filterTableData[rowIndex]
    },
    egrnDocDialogCall (rowId, il_number) {
      this.$refs.egrnDocsDialog.dialogVisible = true
      this.$refs.egrnDocsDialog.rowId = rowId
      this.$refs.egrnDocsDialog.il_number = il_number
      return true
    },
    deleteRow(rowIndex) {
      this.$refs.deleteRecordDialog.dialogVisible = true
      this.$refs.deleteRecordDialog.rowIdForDel = this.filterTableData[rowIndex].id
    },
    paymentHistoryDialogCall(rowId, il_number) {
      this.$refs.paymentsHistoryDialog.dialogVisible = true
      this.$refs.paymentsHistoryDialog.il_base_id = rowId
      this.$refs.paymentsHistoryDialog.il_doc_number = il_number
    }
  },
  computed: {
    filterTableData () {
      let filteredData = this.tableData.filter((data) => {
        let sAddress = false, sFIO = false, sIL = false
        if (this.searchAddress) {  
          if ((data.street + ' ' + data.house + ' - ' + data.appartment).toLowerCase().includes(this.searchAddress.toLowerCase()))
            sAddress = true
        }
        //console.log('######', sAddress)
        if (this.searchFIO) {  
          let FIO_list = data.accounts_il.filter((data_f) => {
            if ((data_f.surname + ' ' + data_f.name + ' ' + data_f.second_name).toLowerCase().includes(this.searchFIO.toLowerCase()))
            return true
          })
          if (FIO_list.length != 0)
            sFIO = true
          
        }

        if (this.searchIL) {
          if (data.il_number.toLowerCase().includes(this.searchIL.toLowerCase()))
            sIL = true
        }

        if (sAddress || sFIO || sIL) {
          return data 
        }
      }) 
    
  
      if (this.searchAddress || this.searchFIO || this.searchIL) {
        //console.log('--------------------', filteredData)
        return filteredData
      }  
      else {
        return this.tableData
      }  
    },
  },
  async mounted() {
    let data = await debt_il_get_all_il_list()
    if (data) {
      data.forEach(element => {
        element.accounts_il.forEach(el => {
          if (!el.passport_il) {
            el.passport_il = {
              id: element.id,
              serial: "",
              number: "",
              who_take: "",
              when_take: "",
              squad_code: "",
              birth_date: "",
              birth_place: "",
              scan: ""
            }
          }
        })
      })
      this.tableData = data
      this.showTable = true
    }
}
  
}
</script>

<style scoped>
.debt-il-wrapper-conteiner {
  border: 1px solid #eee;
  border-radius: 10px;
  /*padding-top: 0.8em;*/
  /*background-color: burlywood;*/
  margin: 1em 2em;
}
.service-title {
  padding-top: 0.8em;
  color: black;
}

.debt-sub-table {
  margin-left: 6em;
}

.filters-row-column {
  margin-top: 2em;
}

.main-button-row-column {
  margin-top: 2em;
  justify-content: right;
}

</style>