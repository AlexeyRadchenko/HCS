<template>
    <div class="mkd-services-works-regester-wrapper-conteiner">
      <el-text class="mx-1" size="large">{{ selectedCompanyId }} - {{ selectedHouseId }}</el-text>
      <el-table :data="tableData" style="width: 100%" max-height="900">
        <el-table-column fixed prop="numOrder" label="№" width="50" />
        <el-table-column fixed prop="numSprav" label="Разд. Справ." width="69" />
        <el-table-column prop="work" label="Наименование работы" width="500" />
        <el-table-column prop="smeta.date" label="Дата сметы" width="100" />
        <el-table-column prop="numSmeta" label="№ Сметы / Файл" width="140">
          <template #default="scope">
            <div style="display: flex; align-items: center">
              <span>{{ scope.row.smeta.num }}</span>
              <span style="margin-left: 10px"><a :href="scope.row.smeta.fileUrl">Документ</a></span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="act.date" label="Дата акта" width="100" />
        <el-table-column prop="act.num" label="№ Акта / Файл" width="140">
          <template #default="scope">
            <div style="display: flex; align-items: center">
              <span>{{ scope.row.act.num }}</span>
              <span style="margin-left: 10px"><a :href="scope.row.act.fileUrl">Документ</a></span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="monthWork" label="Месяц пров. работ" width="100" />
        <el-table-column prop="yearWork" label="Год пров. работ" width="100" />
        <el-table-column prop="sumWork" label="Стоимость работ" width="100" />
        <el-table-column fixed="right" label="Редактирование" min-width="120">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="small"
              @click.prevent="deleteRow(scope.$index)"
            >
              Remove
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-button class="mt-4" style="width: 100%" @click="onAddItem">
        Добавить сведения об услуге/работе
      </el-button>
      <MKDWorkAddModal 
        v-model:dialogMKDWorksAddVisibleSub="showMKDWorkAddModal"
        :house-id="props.selectedHouseId" 
        :company="props.selectedCompanyId"
        :house-name="props.selectedHouseName"
        :work-id="workID"
        />
    </div>
</template>

<script setup>
// Импортируйте необходимые функции, если нужно
import { ref, reactive, computed, onMounted, watch, defineModel, toRaw } from 'vue';
import MKDWorkAddModal from './modal/MKDWorkAddModal.vue';
import { get_mkd_works_get_all_works_by_house_id } from '../../http/mkd-works-http-common'

const props = defineProps({
  selectedHouseId: String,
  selectedCompanyId: String,
  selectedHouseName: String,
})
const showMKDWorkAddModal = ref(false)
const workID =ref('')

const tableData = ref([
  {
    numOrder: 1,
    numSprav: '2.2',
    work: 'Tom',
    smeta: {num:'12/123', fileUrl: 'urlFile', date: '01.01.2024'},
    act: {num:'12/123', fileUrl: 'urlFile', date: '01.02.2024'},
    monthWork: 'сентябрь',
    yearWork: '2024',
    sumWork: '54654.45'

  },
  {
    numOrder: 2,
    numSprav: '2.2',
    work: 'Tom',
    smeta: {num:'12/123', fileUrl: 'urlFile', date: '01.01.2024'},
    act: {num:'12/123', fileUrl: 'urlFile', date: '01.02.2024'},
    monthWork: 'сентябрь',
    yearWork: '2024',
    sumWork: '54654.45'
  },
  {
    numOrder: 3,
    numSprav: '2.2',
    work: 'Tom',
    smeta: {num:'12/123', fileUrl: 'urlFile', date: '01.01.2024'},
    act: {num:'12/123', fileUrl: 'urlFile', date: '01.02.2024'},
    monthWork: 'сентябрь',
    yearWork: '2024',
    sumWork: '54654.45'
  },
])

const deleteRow = (index) => {
  tableData.value.splice(index, 1)
}

const onAddItem = () => {
  if (!props.selectedHouseId) {
    return
  }
  showMKDWorkAddModal.value = true
  workID.value = ''
}

watch(() => props.selectedHouseId, (oldSelectedHouseId, newSelectedHouseId) => {
  console.log("newProps", newSelectedHouseId)
  get_mkd_works_get_all_works_by_house_id(newSelectedHouseId).then((response) => {
    console.log(response)
  }).catch((error) => {
    console.error('Error:', error);
  });
})

const worksDataFromDBtoTableView = (worksData) => {
  for (let [index, element] of worksData.entries()) {
    tableData.value.push({
      numOrder: index + 1,
      numSprav: element.numsprav,
      work: element.work,
      smeta: {num:element.smeta.num, fileUrl: element.smeta.fileUrl, date: element.smeta.date},
      act: {num:element.act.num, fileUrl: element.act.fileUrl, date: element.act.date},
      monthWork: element.monthWork,
      yearWork: element.yearWork,
      sumWork: element.sumWork,
    })
  }
}


onMounted(() => {
  console.log('Компонент был смонтирован!');
  console.log('props!', props.selectedHouseId);
  get_mkd_works_get_all_works_by_house_id(props.selectedHouseId).then((response) => {
    console.log(response)
  }).catch((error) => {
    console.error('Error:', error);
  });
  //console.log('selectedCompanyId:', selectedCompanyId);
  //console.log('selectedHouseId:', selectedHouseId);
});
</script>

<style scoped>

</style>
  