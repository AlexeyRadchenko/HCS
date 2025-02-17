<template>
    <div class="mkd-services-wrapper-conteiner">
        <el-container >
            <el-header>
                <el-row>
                    <el-col :span="8"><div class="service-title"><el-text><h1>{{ serviceTitle }}</h1></el-text></div></el-col>  
                    <el-col :span="11"><div></div></el-col>
                    <el-col :span="3"><div class="all-works-regestry-btn-wrapper"><el-button type="primary" @click="dialogWorksRegistryMain = true">Реестр актов формы КС-2</el-button></div></el-col>
                    <el-col :span="2"><div class="all-works-btn-wrapper"><el-button type="primary" @click="dialogTypeOfWorksTableVisibleMain = true">Виды работ</el-button></div></el-col>
                </el-row>  
            </el-header>
            <el-container style="height: 49em">
              <el-aside width="250px">
                <el-scrollbar>
                  <el-menu :default-openeds="['1', '2']" @open="handleOpen" default-active="1-50">
                    <el-sub-menu index="1">
                      <template #title>
                        <font-awesome-icon :icon="['fas', 'house']" /><span class="mkd-services-asaide-menu-title">Комфортный дом</span>
                      </template>
                      <template v-for="house in houses_komf" :key="house.id">
                        <el-menu-item :index="'1-' + house.id" @click="handleMenuItemClick">{{  house.house }}</el-menu-item>
                      </template>  
                    </el-sub-menu>
                    <el-sub-menu index="2">
                      <template #title>
                        <font-awesome-icon :icon="['fas', 'house']" /><span class="mkd-services-asaide-menu-title">ЖКС - Трехгорный</span>
                      </template>
                      <template v-for="house in houses_jks" :key="house.id">
                        <el-menu-item :index="'1-' + house.id" @click="handleMenuItemClick">{{  house.house }}</el-menu-item>
                      </template>
                    </el-sub-menu>
                  </el-menu>
                </el-scrollbar>
              </el-aside>
              <el-main>
                  <el-row>
                    <el-col :span="24">
                      <el-tabs type="border-card" v-model="activeTabMain">
                        <el-tab-pane label="Выполненные работы">
                          <WorksRegester
                          :selected-house-id="selectedHouseId"
                          :selected-company-id="selectedCompanyId"
                          :selected-house-name="getSelectedHouse"
                          :all-works-ref="works_refrenece_book_list"
                          :works-periods-ref="periodsNames"
                            />
                        </el-tab-pane>
                        <el-tab-pane label="Годовые акты выполенных работ">
                          <MKDYearWorksActs
                          :selected-house-id="selectedHouseId"
                          :selected-company-id="selectedCompanyId"
                          :selected-house-name="getSelectedHouse"
                          :active-tab-year="activeTabMain"
                            />
                        </el-tab-pane>
                        <el-tab-pane label="Тех. Документация">
                          <MKDTechnicDocs
                          :selected-house-id="selectedHouseId"
                          :selected-company-id="selectedCompanyId"
                          :selected-house-name="getSelectedHouse"
                          :active-tab-tech-doc="activeTabMain"
                            />
                        </el-tab-pane>
                        <el-tab-pane label="Фотофиксация работ"></el-tab-pane>
                        <el-tab-pane label="Фотофиксация аварий"></el-tab-pane>
                      </el-tabs>     
                    </el-col>
                  </el-row>
                  <el-row></el-row>
              </el-main>
            </el-container>
        </el-container>
        <MKDAllWorksRegestry v-model:dialogAllWorksRegisterVisibleSub="dialogWorksRegistryMain" />
        <WorkTypesModal
         v-model:dialogTypeOfWorksTableVisibleSub="dialogTypeOfWorksTableVisibleMain"
         :works-main-ref-book="works_ref_from_db.mainworks"
         :works-sub-ref-book="works_ref_from_db.subworks"
         :works-fix-ref-book="works_ref_from_db.fixworks"
          />
    </div>
  </template>
  
<script setup>
// Импортируйте необходимые функции, если нужно
import { ref, reactive, computed, onMounted, watchPostEffect } from 'vue';
import WorkTypesModal from './modal/WorkTypesModal.vue';
import WorksRegester from './WorksRegester.vue';
import MKDAllWorksRegestry from './modal/MKDAllWorksRegestry.vue';
import MKDYearWorksActs from './MKDYearWorksActs.vue';
import MKDTechnicDocs from './MKDTechnicDocs.vue';
import { get_mkd_works_get_all_houses, get_works_reference_book } from '../../http/mkd-works-http-common';
// Создайте реактивные переменные
const serviceTitle = ref('Оказанные услуги (работы по МКД)')
const dialogTypeOfWorksTableVisibleMain = ref(false)
const dialogWorksRegistryMain = ref(false)
const selectedHouseId = ref('50')
const selectedCompanyId = ref('1')

// Логика для компонента
const count = ref(0);
const houses_komf = ref([])
const houses_jks = ref([])
const works_refrenece_book_list = ref([])
const works_periods = ref([])
const works_ref_from_db = ref({
  mainworks: [],
  subworks: [],
  fixworks: [],
})

const activeTabMain = ref('0')
const getSelectedHouse = computed(() => {
  //console.log("houses", houses_komf.value, )
  return houses_komf.value.find(house => String(house.id) === selectedHouseId.value)?.house
})

const periodsNames = computed(() => { 
    let options = works_periods.value.map((item, idx) => {
    return {
      value: idx,
      label: item
    }
  })
  //console.log('Options', options)
  return options
})


const increment = () => {
  count.value++;
};
const handleOpen = (key, keyPath) => {
  console.log(key, keyPath)
}

const handleMenuItemClick = (item) => {
  const companyIdhouseId = item.index.split('-')
  selectedCompanyId.value = companyIdhouseId[0];
  selectedHouseId.value = companyIdhouseId[1];
  console.log(item, companyIdhouseId)
}
onMounted(() => {
  console.log('Компонент был смонтирован!');
  get_mkd_works_get_all_houses().then((response) => {
    //console.log('Data:', response.data);
    response.data.forEach(element => {
      if (element.company_id === 1) {
          houses_komf.value.push({
          id: element.id,
          house: element.street + ' - ' + element.number,
        })
      }

      if (element.company_id === 2) {
          houses_jks.value.push({
          id: element.id,
          house: element.street + ' - ' + element.number,
        })
      }
      
    });
    houses_komf.value.sort((a, b ) => a.house > b.house ? 1: -1)
    houses_jks.value.sort((a, b ) => a.house > b.house ? 1: -1)
  }).catch((error) => {
    console.error('Error:', error);
  });

  get_works_reference_book().then((response) => {
    //console.log('Data:RESPOSE', response.data);
    Object.assign(works_ref_from_db.value, response.data)
    for (const element of response.data.mainworks) {
      //console.log('Data:RESPOSE', element);
      works_refrenece_book_list.value.push(
        {
          value: String(element.id),
          label: element.work,
          wtype: element.workType,
        }
      )

      for (const subworks of response.data.subworks) {
        if (subworks.mainwork_id === element.id) {
          works_refrenece_book_list.value.push(
            {
              value: element.id+'_1_'+subworks.id,
              label: subworks.work,
            }
          )
        }
      if(!works_periods.value.includes(subworks.period) && subworks.period != '') {
          works_periods.value.push(subworks.period)
        }
      }

      for (const fixwork of response.data.fixworks) {
        if (fixwork.mainwork_id === element.id) {
          works_refrenece_book_list.value.push(
            {
              value: element.id+'_2_'+fixwork.id,
              label: fixwork.work,
            }
          )
        }
        if(!works_periods.value.includes(fixwork.period) && fixwork.period != '') {
          works_periods.value.push(fixwork.period)
        }
      }
    }
  }).catch((error) => {
    console.error('Error:', error);
  });

});
</script>

<style scoped>
.mkd-services-wrapper-conteiner {
  border: 1px solid #eee;
  border-radius: 10px;
  /*padding-top: 0.8em;*/
  /*background-color: burlywood;*/
  margin: 1em 2em;
  min-height: 53em;
}
.service-title {
  padding-top: 0.8em;
  color: black;
}

.debt-sub-table {
  margin-left: 4em;
}

.all-works-btn-wrapper{
  padding-top: 0.8em;
  text-align: right;
}
.all-works-regestry-btn-wrapper {
  padding-top: 0.8em;
  text-align: right;
}
.mkd-services-asaide-menu-title {
  margin-left: 1em;
}
</style>
  