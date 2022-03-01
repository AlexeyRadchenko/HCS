<template>
  <el-container class="contacts-wrapper-conteiner">
    <el-header>
      <el-row>
        <el-col :span="4"><div class="service-title"><h1>{{ serviceTitle }}</h1></div></el-col>  
        <el-col :span="16"><div></div></el-col>
        <el-col :span="4"><div class="new-contact-btn-wrapper"><el-button type="primary" @click="dialogVisible = true">Добавить запись</el-button></div></el-col>
      </el-row>  
    </el-header>
      <el-container v-loading="dataLoading">
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
                      <el-button color="#626aef" style="color: white" class="scrollbar-address-item" type="primary" @click="handleClickStreetHouse(item)">{{ item }}</el-button>
                    </div>
                  </el-collapse-item>
                  <el-collapse-item title="ЖилКомСервис - Трехгорный" name="2">
                    <div class="search-houses-wrapper">
                      <el-input v-model="streetHouseSearchValueJKS" placeholder="улица или номер дома" clearable />
                    </div>
                    <div v-for="(item, index) in StreetsHousesJKSFilteredList" :key="item" style="margin: 10px;">
                      <el-button color="#626aef" style="color: white" class="scrollbar-address-item" type="primary" @click="handleClickStreetHouse(item)">{{ item }}</el-button>
                    </div> 
                  </el-collapse-item>   
                </el-collapse>
              </el-scrollbar>
            </el-main>
          </el-container>
        </el-aside>
        <el-main>
          <el-container>
            <el-row>
              <el-col :span="24">
                <div class="tags-wrapper">
                  <el-tag
                    v-for="tag in dynamicTags"
                    :key="tag"
                    class="tag-space"
                    closable
                    :disable-transitions="false"
                    @close="handleClose(tag)"
                    >
                    {{ tag }}
                  </el-tag>
                </div>
              </el-col>
            </el-row>
          </el-container>
          <el-container>
            <el-row >
              <el-col :span="24">
                <el-table
                  :data="pagedTableData"
                  stripe
                  style="width: 100%">
                  <el-table-column prop="house" label="Дом" width="180" />
                  <el-table-column prop="entrance" label="Подъезд" width="80" align="center" />
                  <el-table-column prop="appartment" label="Квартира" width="85" align="center" />
                  <el-table-column prop="FIO" label="ФИО" width="300" header-align="center" align="center">
                      <template #header>
                      <el-input v-model="searchFIO" size="small" placeholder="Type to search" clearable />
                      </template>
                  </el-table-column>
                  <el-table-column prop="part_have" label="Доля имущества" width="135" align="center" />
                  <el-table-column prop="home_phone" label="Домашный тел." width="135" />
                  <el-table-column prop="work_phone" label="Рабочий тел." width="135" />
                  <el-table-column prop="mobile_phone" label="Мобильный тел." width="140" />
                  <el-table-column prop="email" label="Электронная почта" width="180" />
                  <el-table-column prop="note" label="Примечание" width="180" />
                </el-table>
              </el-col>
            </el-row>
          </el-container>
          <el-container>
            <el-row >
                <el-col :span="24">
                  <div class="pagination-wrapper">
                    <el-pagination
                    background
                    layout="prev, pager, next"
                    :total="filteredByHouseTableData.length"
                    :page-size="pageSize"
                    @current-change="setPage"
                    >
                    </el-pagination>
                  </div>   
                </el-col>
            </el-row>
          </el-container>    
        </el-main>
      </el-container>
          <el-dialog
            v-model="dialogVisible"
            title="Добавление новой записи"
            width="50%"
            :before-close="handleCloseModalW"
          >
            <ContactsModal :modalKomfAddresses="komfAddresses" :modalJKSAddresses="JKSAddresses" />
            <template #footer>
              <span class="dialog-footer">
                <el-button @click="dialogVisible = false">Отмена</el-button>
                <el-button type="primary" @click="dialogVisible = false"
                  >Сохранить</el-button
                >
              </span>
            </template>
          </el-dialog>
  </el-container>
</template>

<script>
import { get_addresses_house_street_by_org_id, get_contacts_list } from '../http/http-common';
import { handleAddresses, serverDataToTableRows } from '../utils/utils';
import { ElMessageBox } from 'element-plus';
import ContactsModal from './ContactsModal.vue'

// <p v-for="(item, index) in StreetsHousesKomfFilteredList" :key="item" class="scrollbar-address-item">{{ item }}</p> 
export default {
    components: {
      ContactsModal
    },
    data() {
      return {
        tableData: [],
        filteredByHouseTableData: [],
        searchFIO: '',
        serviceTitle: 'Справочник',
        loading: true,
        streetHouseSearchValueKomf: '',
        streetsHousesKomf: [],
        streetHouseSearchValueJKS: '',
        streetsHousesJKS: [],
        activeNames: ['1'],
        dataLoading: true,
        activeName: 'first',
        dynamicTags: [],
        pageSize: 15,
        page: 1,
        dialogVisible: false,
        komfAddresses: [],
        JKSAddresses: [],
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
      searchData(dataTable) {
        var fDT = dataTable.filter(data => !this.search || data.FIO.toLowerCase().includes(this.search.toLowerCase()))
        return fDT.slice(this.pageSize * this.page - this.pageSize, this.pageSize * this.page)
      },
      handleClickStreetHouse (item) {
        if (!this.dynamicTags.includes(item)) {
          this.dynamicTags.push(item)
        }
      },
      handleClose (tag) {
        this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1)
      },
      setPage (val) {
        this.page = val
      },
      handleCloseModalW (done) {
        ElMessageBox.confirm('Are you sure to close this dialog?')
        .then(function () {
            done();
        })
        .catch(function () {
            // catch error
        })
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
      },
      pagedTableData() {
        this.filteredByHouseTableData = this.tableData.filter((row) => {
          if (this.dynamicTags.length) {
            console.log('first')
            return this.dynamicTags.includes(row.house)
          }
          return true
        })
        if (this.searchFIO){
          this.filteredByHouseTableData = this.filteredByHouseTableData.filter(data => !this.searchFIO || data.FIO.toLowerCase().includes(this.searchFIO.toLowerCase()))
        }
        
        return this.filteredByHouseTableData.slice(this.pageSize * this.page - this.pageSize, this.pageSize * this.page)
     }
    },
    async mounted() {
      this.komfAddresses = await get_addresses_house_street_by_org_id(1)
      this.JKSAddresses = await get_addresses_house_street_by_org_id(2)
      var servContacts = await get_contacts_list()
      this.tableData = await serverDataToTableRows(servContacts)
      this.streetsHousesKomf = await handleAddresses(this.komfAddresses)
      this.streetsHousesJKS = await handleAddresses(this.JKSAddresses)
      this.dataLoading = false
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

.el-row {
  margin-bottom: 20px;
  width: 100%;
}
.el-row:last-child {
  margin-bottom: 0;
}
.pagination-wrapper {
  margin-top: 20px;
  text-align: center;
}
.tag-space {
  margin: 0.3em;
}
.tags-wrapper {
  min-height: 31.19px;
}

.new-contact-btn-wrapper {
  padding-top: 0.8em;
  text-align: right;
}

</style>
