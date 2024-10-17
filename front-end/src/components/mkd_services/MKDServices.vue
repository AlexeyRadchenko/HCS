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
            <el-container>
              <el-aside width="300px">
                <el-scrollbar>
                  <el-menu :default-openeds="['1', '2']" @open="handleOpen">
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
                        <el-menu-item index="2-1" @click="handleMenuItemClick">Option 1</el-menu-item>
                        <el-menu-item index="2-2">Option 2</el-menu-item>
                    </el-sub-menu>
                  </el-menu>
                </el-scrollbar>
              </el-aside>
              <el-main>
                  <el-row>
                    <el-col :span="24">
                      <el-tabs type="border-card">
                        <el-tab-pane label="Акты выполненных работ">
                          <WorksRegester
                          :selected-house-id="selectedHouseId"
                          :selected-company-id="selectedCompanyId"
                          :selected-house-name="getSelectedHouse"
                            />
                        </el-tab-pane>
                        <el-tab-pane label="Годовые акты выполенных работ">
                          <MKDYearWorksActs
                          :selected-house-id="selectedHouseId"
                          :selected-company-id="selectedCompanyId"
                          :selected-house-name="getSelectedHouse"
                            />
                        </el-tab-pane>
                        <el-tab-pane label="Тех. Документация">
                          <MKDTechnicDocs
                          :selected-house-id="selectedHouseId"
                          :selected-company-id="selectedCompanyId"
                          :selected-house-name="getSelectedHouse"
                            />
                        </el-tab-pane>
                      </el-tabs>     
                    </el-col>
                  </el-row>
                  <el-row></el-row>
              </el-main>
            </el-container>
        </el-container>
        <MKDAllWorksRegestry v-model:dialogAllWorksRegisterVisibleSub="dialogWorksRegistryMain" />
        <WorkTypesModal v-model:dialogTypeOfWorksTableVisibleSub="dialogTypeOfWorksTableVisibleMain" />
    </div>
  </template>
  
<script setup>
// Импортируйте необходимые функции, если нужно
import { ref, reactive, computed, onMounted } from 'vue';
import WorkTypesModal from './modal/WorkTypesModal.vue';
import WorksRegester from './WorksRegester.vue';
import MKDAllWorksRegestry from './modal/MKDAllWorksRegestry.vue';
import MKDYearWorksActs from './MKDYearWorksActs.vue';
import MKDTechnicDocs from './MKDTechnicDocs.vue';
import { get_mkd_works_all_data } from '../../http/mkd-works-http-common';
// Создайте реактивные переменные
const message = ref('Привет, Vue 3!');
const serviceTitle = ref('Оказанные услуги (работы по МКД)')
const dialogTypeOfWorksTableVisibleMain = ref(false)
const dialogWorksRegistryMain = ref(false)
const selectedHouseId = ref('1')
const selectedCompanyId = ref('1')

// Логика для компонента
const count = ref(0);
const houses_komf = ref([
  {id: '1', house: '50 лет Победы - 22'},
  {id: '2', house: '60 лет Октября - 10'},
  {id: '3', house: 'Володина -12'}
])
const getSelectedHouse = computed(() => {
  return houses_komf.value.find(house => house.id === selectedHouseId.value)?.house
})
const gridData = [
{
  date: '2016-05-02',
  name: 'John Smith',
  address: 'No.1518,  Jinshajiang Road, Putuo District',
},
{
  date: '2016-05-04',
  name: 'John Smith',
  address: 'No.1518,  Jinshajiang Road, Putuo District',
},
{
  date: '2016-05-01',
  name: 'John Smith',
  address: 'No.1518,  Jinshajiang Road, Putuo District',
},
{
  date: '2016-05-03',
  name: 'John Smith',
  address: 'No.1518,  Jinshajiang Road, Putuo District',
},
]
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
  get_mkd_works_all_data().then((response) => {
    console.log('Data:', response.data);
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
  