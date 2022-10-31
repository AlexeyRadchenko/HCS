<template>
  <el-container class="contacts-wrapper-conteiner">
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
            <el-table :data="tableData"  row-key="id" style="width: 100%" height="250" :tree-props="{ children: 'people', hasChildren: 'multi'}" >
              <el-table-column fixed prop="address" label="Адрес" width="150" />
              <el-table-column fixed prop="sobst" label="Собственность" width="150" />
              <el-table-column fixed prop="date" label="Част./Соц. найм" width="150" />
              <el-table-column prop="name" label="Физ. Лица" width="120" />
              <el-table-column prop="state" label="Дата и/произиводства" width="120" />
              <el-table-column prop="city" label="№ исполнительного производства" width="320" />
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
            id: 1,
            address: 'Строителей - 1',
            sum: 123,
            sobst: 'Частная',
            date: '2016-05-02',
            name: 'Tom',
            multi: false,
          },
          {
            id: 2,
            address: 'Строителей - 1',
            sum: 123,
            date: '2016-05-02',
            sobst: 'Частная',
            name: 'Tom',
            multi: false,
          },
          {
            id: 3,
            address: 'Строителей - 1',
            sum: 123,
            sobst: 'Частная',
            date: '2016-05-04',
            name: 'Tom',
            multi: false,
            people: [
              {
                id: 31,
                date: '2016-05-01',
                name: 'wangxiaohu',
              },
              {
                id: 32,
                date: '2016-05-01',
                name: 'wangxiaohu',
              },
            ],
          },
          {
            id: 4,
            address: 'Строителей - 1',
            sum: 123,
            sobst: 'Частная',
            date: '2016-05-01',
            name: 'Tom',
            multi: true,
          },
          {
            id: 5,
            address: 'Строителей - 1',
            sum: 123,
            sobst: 'Частная',
            date: '2016-05-08',
            name: 'Tom',
            multi: true,
          },
          {
            id: 6,
            address: 'Строителей - 1',
            sum: 123,
            sobst: 'Частная',
            date: '2016-05-06',
            name: 'Tom',
            multi: true,
          },
          {
            id: 7,
            address: 'Строителей - 1',
            sum: 123,
            sobst: 'Частная',
            date: '2016-05-07',
            name: 'Tom',
            multi: true,
          },
        ],

    }
  }
}
</script>

<style scoped>
.contacts-wrapper-conteiner {
  border: 1px solid #eee;
  border-radius: 10px;
  /*padding-top: 0.8em;*/
  /*background-color: burlywood;*/
  margin: 1em 2em;
  height:100%;
}
.service-title {
  padding-top: 0.8em;
  color: black;
}
.table-container {
  width: 100%;
  margin-top:2em;
}
</style>