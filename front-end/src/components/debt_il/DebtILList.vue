<template>
  <el-container class="debt-il-wrapper-conteiner">
    <el-header>
      <el-row>
        <el-col :span="8"><div class="service-title"><h1>{{ serviceTitle }}</h1></div></el-col>  
        <el-col :span="12"><div></div></el-col>
        <el-col :span="4"><div class="new-contact-btn-wrapper"><el-button type="primary" @click="dialogVisible = true">Добавить запись</el-button></div></el-col>
      </el-row>  
    </el-header>
    <el-container class="table-container">
      <el-row>
        <el-col :span="24">
          <div>
            <el-table :data="tableData"  row-key="id" style="width: 100%">
              <el-table-column type="expand">
                <template #default="props">
                  <div class="debt-sub-table">
                    <p><span>Адрес:</span> {{ props.row.street }} {{ props.row.house }} - {{ props.row.appartment }}</p>
                    <h2>Физ. лица</h2>
                    <el-table :data="props.row.accounts_il">
                      <el-table-column label="Лицевой счет" prop="account_number" />
                      <el-table-column label="ФИО" prop="name"/>
                      <el-table-column label="Дата рождения" prop="name"/>
                    </el-table>
                  </div>
                </template>
              </el-table-column>
              <el-table-column fixed label="Адрес" width="180" :formatter="addressTableFormatter" />
              <el-table-column fixed prop="sobst"  label="Собственность" width="125" />
              <el-table-column fixed prop="date" :formatter="typeOwnFormatter" label="Част./Соц. найм" width="150" />
              <el-table-column fixed prop="city" label="№ исполнительного производства" width="120" />
              <el-table-column prop="name" label="Физ. Лица" width="120" />
              <el-table-column prop="state" label="Дата и/произиводства" width="120" />
              <el-table-column prop="sum" label="Сумма долга" width="120" />
              <el-table-column prop="zip" label="Сумма госпошлины" width="120" />
              <el-table-column prop="zip" label="Просуженный период" width="120" />
              <el-table-column prop="zip" label="Дата окончания произодства" width="120" />
              <el-table-column prop="zip" label="Сумма взысканной задолженности" width="120" />
              <el-table-column prop="zip" label="Причина окончания произодства" width="120" />
              <el-table-column prop="zip" label="Примечание" width="120" />
            </el-table>
          </div>
        </el-col>  
      </el-row>  
    </el-container>  
  </el-container>  
</template>

<script>
export default {
  components: {
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
                second_name: "string",
                surname: "string",
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
            property_self: true,
            il_number: "string",
            il_date: "2022-11-02T10:56:04.116Z",
            ur_in_work: true,
            gov_tax: 0,
            order_cancel: true,
            bailiff_forward_date: "2022-11-02T10:56:04.116Z",
            start_exec_pross_date: "2022-11-02T10:56:04.116Z",
            sum_all_get: 0,
            sum_not_yet_get: 0,
            payments: 0,
            payments_il: [
              {
                id: 0,
                date: "2022-11-02T10:56:04.116Z",
                type: "string",
                sum: 0
              }
            ],
            debt_sum: 0,
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
.table-container {
  width: 100%;
  margin-top:2em;
  height: 95%
}
.debt-sub-table {
  margin-left: 4em;
}
</style>