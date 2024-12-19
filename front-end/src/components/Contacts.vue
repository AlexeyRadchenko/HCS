<template>
  <el-container class="contacts-wrapper-conteiner" >
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
                <el-collapse v-model="activeNames" @change="handleChange" class="scroll-side-bar-item">
                  <el-collapse-item title="Комфортный дом" name="1" >
                    <div class="search-houses-wrapper">
                      <el-input v-model="streetHouseSearchValueKomf" placeholder="улица или номер дома" clearable />
                    </div>
                    <div v-for="item in StreetsHousesKomfFilteredList" :key="item" style="margin: 10px;">
                      <el-button color="#626aef" style="color: white" class="scrollbar-address-item" type="primary" @click="handleClickStreetHouse(item)">{{ item }}</el-button>
                    </div>
                  </el-collapse-item>
                  <el-collapse-item title="ЖилКомСервис - Трехгорный" name="2">
                    <div class="search-houses-wrapper">
                      <el-input v-model="streetHouseSearchValueJKS" placeholder="улица или номер дома" clearable />
                    </div>
                    <div v-for="item in StreetsHousesJKSFilteredList" :key="item" style="margin: 10px;">
                      <el-button color="#626aef" class="scrollbar-address-item" type="primary" @click="handleClickStreetHouse(item)">{{ item }}</el-button>
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
              <el-col :span="24" :xl="24" :sm="24" :md="24" :lg="24">
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
              <el-col :span="24" :xl="24" :sm="24" :md="24" :lg="24">
                <el-table
                  :data="pagedTableData"
                  stripe
                  style="width: 100%">
                  <el-table-column prop="house" label="Дом" min-width="75em" />
                  <el-table-column prop="entrance" label="Под." min-width="32em" align="center" />
                  <el-table-column prop="appartment" label="Кв." min-width="26em" align="center" />
                  <el-table-column prop="FIO" label="ФИО" min-width="110em" header-align="center" align="center">
                      <template #header>
                      <el-input v-model="searchFIO" size="small" placeholder="Поиск по ФИО" clearable />
                      </template>
                  </el-table-column>
                  <el-table-column prop="part_have" label="Доля имущества" min-width="70em" align="center" />
                  <el-table-column prop="home_phone" label="Домашный тел." min-width="64em" align="center" />
                  <el-table-column prop="work_phone" label="Рабочий тел." min-width="56em" align="center" />
                  <el-table-column prop="mobile_phone" label="Мобильный тел." min-width="66em" align="center" />
                  <el-table-column prop="email" label="Эл. почта" min-width="56em" align="center" />
                  <el-table-column label="Прим." min-width="30em" header-align="center" align="center">
                    <template #default="scope">
                      <el-popover effect="light" trigger="hover" placement="top" width="auto">
                        <template #default>
                          <div>Примечание</div>
                          <div>{{ scope.row.note }}</div>
                        </template>
                        <template #reference>
                          <el-tag>Прим.</el-tag>
                        </template>
                      </el-popover>
                    </template>
                  </el-table-column>
                  <el-table-column label="Изм./удал." header-align="center" align="center">
                    <template #default="scope">
                      <div class="flex flex-wrap items-center">
                        <el-dropdown trigger="click" >
                          <el-button type="primary">
                            Изм./удал.<font-awesome-icon :icon="['fas', 'angle-down']" size="1x" />
                          </el-button>
                          <template #dropdown>
                            <el-dropdown-menu>
                              <el-dropdown-item>
                                <el-button size="large" round @click="handleEditTableRow(scope.$index, scope.row)"
                                  >Редакт.</el-button
                                >
                              </el-dropdown-item>
                              <el-dropdown-item>
                                <el-button size="large" round type="danger"
                                  @click="handleDeleteTableRow(scope.$index, scope.row)"
                                  >Удалить</el-button
                                >
                              </el-dropdown-item>  
                            </el-dropdown-menu>
                          </template>
                        </el-dropdown>
                      </div>  
                    </template>
                  </el-table-column>
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
          >
            <ContactsModal :modalKomfAddresses="komfAddresses" :modalJKSAddresses="JKSAddresses" :formDataModal="formData" />
            <template #footer>
              <span class="dialog-footer">
                <el-button @click="dialogVisible = false">Отмена</el-button>
                <el-button type="primary" @click="sendFormModalData"
                  >Сохранить</el-button
                >
              </span>
            </template>
          </el-dialog>
          <el-dialog
            v-model="dialogDelVisible"
            title="Удаление записи"
            width="35%"
          >
            <el-row><span>Вы действительно хотите удалить эту запись ?</span></el-row>
            <el-row :gutter="20" class="row-bg">
                    <el-col :span="6">{{ formData.street_house }}</el-col>
                    <el-col :span="3">под. {{ formData.entrance}}</el-col>
                    <el-col :span="3">кв. {{ formData.appartment}}</el-col>
                    <el-col :span="12">{{ formData.name }} {{ formData.second_name }} {{ formData.surname }}</el-col>
            </el-row>

            <span></span><span></span>
            <template #footer>
              <span class="dialog-footer">
                <el-button @click="dialogDelVisible = false">Отмена</el-button>
                <el-button type="danger" @click="sendDelFormModalData"
                  >Да</el-button
                >
              </span>
            </template>
          </el-dialog>
  </el-container>
</template>

<script>
import { get_addresses_house_street_by_org_id, get_contacts_list,
       create_new_record_in_contacts, update_record_in_contacts, delete_record_in_contacts } from '../http/http-common';
import { handleAddresses, serverDataToTableRows, getModalFormObject, ContactDataObjectToTableObject } from '../utils/utils';
import { useContactStore } from '../storage/contactService';
import ContactsModal from './ContactsModal.vue';
import { useAuthStore } from '../storage/auth';
import { reactive } from '@vue/reactivity';


export default {
    components: {
      ContactsModal
    },
    setup() {
      let contactsStore = useContactStore()
      const authStore = useAuthStore()
      let reactiveTableData = reactive (contactsStore.getContactsServiceTableData)
      return { contactsStore, authStore, reactiveTableData }
    },
    data() {
      return {
        //tableData: [],
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
        dialogDelVisible: false,
        komfAddresses: [],
        JKSAddresses: [],
        formData: {
          uuid: '',
          name: '',
          second_name: '',
          surname: '',
          street_house: '',
          entrance: '',
          appartment: '',
          part_own: '',
          mobile_phones: '',
          home_phones: '',
          work_phones: '',
          emails: '',
          note: '',
          system_user: this.authStore.getUser.login
        },
      } 
    },
    methods: {
      init_form_data(row) {
        this.formData.uuid = row.uuid
        this.formData.name = row.FIO.split(' ')[0]
        this.formData.second_name = row.FIO.split(' ')[1]
        this.formData.surname = row.FIO.split(' ')[2]
        this.formData.street_house = row.house
        this.formData.entrance = row.entrance
        this.formData.appartment = row.appartment
        this.formData.part_own = row.part_have
        this.formData.home_phones = row.home_phone
        this.formData.mobile_phones = row.mobile_phone
        this.formData.work_phones = row.work_phone
        this.formData.emails = row.email
        this.formData.note = row.note
      },
      handleEditTableRow(index, row) {
        this.init_form_data(row)
        this.dialogVisible = true
      },
      handleDeleteTableRow(index, row) {
        this.init_form_data(row)
        this.dialogDelVisible = true
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
      async sendFormModalData () {
        var formData = getModalFormObject(this.formData)
        if (!this.formData.uuid) {
          var response = await create_new_record_in_contacts (formData)
          if (response) {
            var data = await ContactDataObjectToTableObject (this.formData)
            this.contactsStore.$patch((state) => {
              state.contactsServiceTableData.unshift(data)
              state.hasChanged = true
            })
          }
        } else {
          var response = await update_record_in_contacts(formData)
          if (response) {
            var data = await ContactDataObjectToTableObject (this.formData)
            var foundIndex =  this.contactsStore.contactsServiceTableData.findIndex(x => x.uuid == data.uuid);
            this.contactsStore.contactsServiceTableData[foundIndex] = data
            this.contactsStore.setStateStatus(true)
          }
        }      
        this.dialogVisible = false
      },
      async sendDelFormModalData () {
        var formData = getModalFormObject(this.formData)
        var response = await delete_record_in_contacts(formData)
        console.log(response)
        if (response) {
          var foundIndex =  this.contactsStore.contactsServiceTableData.findIndex(x => x.uuid == response.key);
          this.contactsStore.contactsServiceTableData.splice(foundIndex, 1)
          this.contactsStore.setStateStatus(true)
        }
        this.dialogDelVisible = false
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
        this.filteredByHouseTableData = this.contactsStore.getContactsServiceTableData.filter((row) => { 
          if (this.dynamicTags.length) {
            return this.dynamicTags.includes(row.house)
          }   
          return this.contactsStore.getContactsServiceTableData
        })
        
        if (this.contactsStore.changedState) {
          this.contactsStore.setStateStatus(false)
        }

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
      var tabeData = await serverDataToTableRows(servContacts)
      this.contactsStore.setContactsServiceTableData(tabeData)
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
  background-color: #1c100b;
  margin: 1em 2em;
  height:100%;
}

.service-title {
  padding-top: 0.8em;
  color: #bbb7b6;
}
.contacts-sidebar-style {
  width: 16%;
  height: 100%;
  /*border: 1px solid #eee;*/
  border: none;
  margin-top: 1.9em;

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
.scroll-side-bar-item {
  background-color: #1c100b;
}
.search-houses-wrapper {
  margin: 10px;
}
.table-container {
  width:100%;
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
.row-bg {
  background-color: #e09ead;
}



</style>
