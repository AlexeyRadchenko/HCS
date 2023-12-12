<template>
<div class="debt-il-wrapper-conteiner">
  <el-container >
    <el-header>
      <el-row>
        <el-col :span="8"><div class="service-title"><h1>{{ serviceTitle }}</h1></div></el-col>  
        <el-col :span="12"><div></div></el-col>
        <el-col :span="4"><div class="new-contact-btn-wrapper"><el-button type="primary" @click="dialogVisible = true">Добавить запись</el-button></div></el-col>
      </el-row>  
    </el-header>
    <el-main>
      <el-row>
        <el-col :span="24">
            <el-table :data="tableData"  row-key="id" style="width: 100%" max-height="55em">
              <el-table-column label="Адрес" width="180" :formatter="addressTableFormatter" align="center" />
              <el-table-column label="Собственность" width="145" align="center" :formatter="OneOrPartsOwnFormatter" />
              <el-table-column align="center" :formatter="typeOwnFormatter" label="Част./Соц. найм" width="150" />
              <el-table-column prop="il_number" label="№ исполнительного производства"  width="120" align="center" />
              <el-table-column type="expand">
                <template #default="props">
                  <div class="debt-sub-table">
                    <p><span>Адрес:</span> {{ props.row.street }} {{ props.row.house }} - {{ props.row.appartment }} <el-button>Сведения ЕГРН</el-button></p>
                    <h2>Физ. лица</h2>
                    <el-table :data="props.row.accounts_il">
                      <el-table-column label="Лицевой счет" prop="account_number" width="120"/>
                      <el-table-column label="ФИО" :formatter="fioFormatter"/>
                      <el-table-column label="Дата рождения" prop="passport_il.birth_date"/>
                      <el-table-column label="Место рождения" prop="passport_il.birth_city"/>
                      <el-table-column label="Серия и номер паспорта" :formatter="passportFormatter" prop="name"/>
                      <el-table-column label="Кем и когда выдан" :formatter="passportWhoAndWhereFormatter" prop="name"/>
                      <el-table-column label="Код подразделения" prop="squad_code"/>
                      <el-table-column label="Скан паспорта" prop="scan"/>
                    </el-table>
                  </div>
                </template>
              </el-table-column>
              <el-table-column label="Физ. Лица" align="center" width="180">
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
              <el-table-column prop="bailiff_forward_date" label="Период задолженности" width="120" />
              <el-table-column label="Дата окончания произодства" width="120" />
              <el-table-column label="Причина окончания произодства" width="120" />
              <el-table-column label="Примечание" width="120" />
              <el-table-column fixed="right" label="Редактирование" width="120" />
            </el-table>  
        </el-col>  
      </el-row>  
    </el-main>  
  </el-container>
</div>  
</template>

<script>
import moment from 'moment/dist/moment'
import ru from 'moment/dist/locale/ru'

export default {
  components: {
  },
  setup() {
    moment.updateLocale('ru', ru)
    return { moment }
  },
  data() {
    return {
        serviceTitle: 'Задолженность по испольнительным листам',
        tableData: [
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
                  seria: "string",
                  number: "string",
                  who_take: "string",
                  when_take: "2022-11-02T10:56:04.116Z",
                  squad_code: "string",
                  birth_date: "2022-11-02T10:56:04.116Z",
                  birth_city: "string",
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
                  seria: "string",
                  number: "string",
                  who_take: "string",
                  when_take: "2022-11-02T10:56:04.116Z",
                  squad_code: "string",
                  birth_date: "2022-11-02T10:56:04.116Z",
                  birth_city: "string",
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
       ],

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
      return row.seria + ' ' + row.number
    },
    passportWhoAndWhereFormatter (row, column) {
      return row.who_take + ' ' + row.when_take
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
  margin-left: 4em;
}

</style>