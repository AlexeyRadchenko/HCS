<template>
  <el-container class="contacts-wrapper-conteiner">
    <el-header>
      <el-row>
        <el-col :span="4"><div class="service-title"><h1>{{ serviceTitle }}</h1></div></el-col>  
        <el-col :span="20"><div class="grid-content bg-purple-light"></div></el-col>
      </el-row>  
    </el-header>
      <el-container v-if="dataReady">
        <el-aside class="contacts-sidebar-style">
          <el-container>
            <el-main>
              <el-scrollbar class="scrollbar-address">
                <el-collapse v-model="activeNames" @change="handleChange">
                  <el-collapse-item title="Комфортный дом" name="1">
                    <div class="search-houses-wrapper">
                      <el-input v-model="streetHouseSearchValueKomf" placeholder="улица или номер дома" clearable />
                    </div>
                    <div v-for="(item, index) in StreetsHousesKomfFilteredList" :key="item" style="margin: 10px;">
                      <el-button color="#626aef" style="color: white" class="scrollbar-address-item" type="primary">{{ item }}</el-button>
                    </div>
                  </el-collapse-item>
                  <el-collapse-item title="ЖилКомСервис - Трехгорный" name="2">
                    <div class="search-houses-wrapper">
                      <el-input v-model="streetHouseSearchValueJKS" placeholder="улица или номер дома" clearable />
                    </div>
                    <div v-for="(item, index) in StreetsHousesJKSFilteredList" :key="item" style="margin: 10px;">
                      <el-button color="#626aef" style="color: white" class="scrollbar-address-item" type="primary">{{ item }}</el-button>
                    </div> 
                  </el-collapse-item>   
                </el-collapse>
              </el-scrollbar>
            </el-main>
          </el-container>
        </el-aside>
        <el-main>
          <el-container class="table-container">
            <el-row>
              <el-col :span="24"></el-col>
            </el-row>
            <el-row >
              <el-col :span="24">
                <div class="grid-content bg-purple-dark">
                  <el-table
                     :data="tableData"
                     height="100%"
                     stripe
                     style="width: 100%">
                    <el-table-column prop="house" label="Дом" width="180" />
                    <el-table-column prop="entrance" label="Подъезд" width="80" align="center" />
                    <el-table-column prop="appartment" label="Квартира" width="85" align="center" />
                    <el-table-column prop="FIO" label="ФИО" width="300" header-align="center" align="center" />
                    <el-table-column prop="part_have" label="Доля имущества" width="135" align="center" />
                    <el-table-column prop="home_phone" label="Домашный телефон" width="140" />
                    <el-table-column prop="work_phone" label="Рабочий телефон" width="140" />
                    <el-table-column prop="mobile_phone" label="Мобильный телефон" width="140" />
                    <el-table-column prop="email" label="Электронная почта" width="180" />
                    <el-table-column prop="note" label="Примечание" width="180" />
                  </el-table>
                </div>
              </el-col>
            </el-row>
          </el-container>    
        </el-main>
      </el-container>
  </el-container>
</template>

<script>
import { get_addresses_house_street_by_org_id, get_contacts_list } from '../http/http-common';
import { handleAddresses, serverDataToTableRows } from '../utils/utils';
// <p v-for="(item, index) in StreetsHousesKomfFilteredList" :key="item" class="scrollbar-address-item">{{ item }}</p> 
export default {
    data() {
      return {
        tableData: [
          {
            date: '2016-05-03',
            name: 'Tom',
            address: 'No. 189, Grove St, Los Angeles',
          },
          {
            date: '2016-05-02',
            name: 'John',
            address: 'No. 189, Grove St, Los Angeles',
          },
          {
            date: '2016-05-04',
            name: 'Morgan',
            address: 'No. 189, Grove St, Los Angeles',
          },
          {
            date: '2016-05-01',
            name: 'Jessy',
            address: 'No. 200, Grove St, Los Angeles',
          },
        ],
        search: '',
        serviceTitle: 'Справочник',
        loading: true,
        streetHouseSearchValueKomf: '',
        streetsHousesKomf: ['Володина-12','Володина-14', 'Володина-16', 'Мира-27'],
        streetHouseSearchValueJKS: '',
        streetsHousesJKS: ['Володина-12','Володина-14', 'Володина-16', 'Мира-27'],
        activeNames: ['1'],
        dataReady: false,
        activeName: 'first'
      } 
    },
    methods: {
      handleEdit(index, row) {
        console.log(index, row)
      },
      handleDelete(index, row) {
        console.log(index, row)
      },
      handleChange (val) {
        console.log(val)
      },
      createAlarm() {
        console.log('Create moment!!!')
      },
      handleClickTab (tab, event) {
        console.log(tab, event)
      }
    },
    computed: {
      StreetsHousesKomfFilteredList() {
        return this.streetsHousesKomf.filter((street) => {
          return this.streetHouseSearchValueKomf.toLowerCase().split(' - ').every(v => street.toLowerCase().includes(v));
        });
      },
      StreetsHousesJKSFilteredList() {
        return this.streetsHousesJKS.filter((street) => {
          return this.streetHouseSearchValueJKS.toLowerCase().split(' - ').every(v => street.toLowerCase().includes(v));
        });
      }
    },
    async mounted() {
      var komfAddresses = await get_addresses_house_street_by_org_id(1)
      var JKSAddresses = await get_addresses_house_street_by_org_id(2)
      var servContacts = await get_contacts_list()
      this.tableData = await serverDataToTableRows(servContacts)
      this.streetsHousesKomf = await handleAddresses(komfAddresses)
      this.streetsHousesJKS = await handleAddresses(JKSAddresses)
      this.dataReady = true
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
.contacts-sidebar-style {
  width: 300px;
  height: 100%;
  border: 1px solid #eee;
}
.scrollbar-address{
  height: 47.3rem;
}
.scrollbar-address-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 27px;
  width: 100%;
  text-align: center;
  border-radius: 4px;
  /*background: var(--el-color-primary-light-9);
  //color: var(--el-color-primary);*/
}
.search-houses-wrapper {
  margin: 10px;
}
.table-container {
  width:100%
}

</style>
