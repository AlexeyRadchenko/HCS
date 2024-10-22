<template>
    <div class="mkd-services-works-regester-wrapper-conteiner">
      <el-text class="mx-1" size="large">{{ selectedCompanyId }} - {{ selectedHouseId }}</el-text>
      <el-table :data="tableData" style="width: 100%" max-height="900">
        <el-table-column fixed prop="numOrder" label="№" width="50" />
        <el-table-column prop="worksType" label="Вид работ" width="500" />
        <el-table-column prop="smeta.date" label="Дата сметы" width="100" />
        <el-table-column prop="numSmeta" label="№ Сметы / Файл" width="140">
          <template #default="scope">
            <div style="display: flex; align-items: center">
              <span>{{ scope.row.smeta.num }}</span>
              <span style="margin-left: 10px"><a href="#">{{ scope.row.smeta.fileUrl }}</a></span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="akt.date" label="Дата акта" width="100" />
        <el-table-column prop="akt" label="№ Акта / Файл" width="140">
          <template #default="scope">
            <div style="display: flex; align-items: center">
              <span>{{ scope.row.smeta.num }}</span>
              <span style="margin-left: 10px"><a href="#">{{ scope.row.smeta.fileUrl }}</a></span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="sumNow" label="Текущая цена" width="120" />
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
import dayjs from 'dayjs'

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
    worksType: 'Tom',
    smeta: {num:'12/123', fileUrl: 'urlFile', date: '01.01.2024'},
    akt: {num:'12/123', fileUrl: 'urlFile', date: '01.02.2024'},
    sumNow: 'Los Angeles',
  },
  {
    numOrder: 2,
    worksType: 'Tom',
    smeta: {num:'12/123', fileUrl: 'urlFile', date: '01.01.2024'},
    akt: {num:'12/123', fileUrl: 'urlFile', date: '01.02.2024'},
    sumNow: 'Los Angeles',
  },
  {
    numOrder: 3,
    worksType: 'Tom',
    smeta: {num:'12/123', fileUrl: 'urlFile', date: '01.01.2024'},
    akt: {num:'12/123', fileUrl: 'urlFile', date: '01.02.2024'},
    sumNow: 'Los Angeles',
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
  var order = tableData.value.length + 1
  tableData.value.push({
    numOrder: order,
    worksType: 'Tom',
    smeta: {num:'12/123', fileUrl: 'urlFile'},
    akt: {num:'12/123', fileUrl: 'urlFile'},
    sumNow: 'Los Angeles',
  })
}


onMounted(() => {
  console.log('Компонент был смонтирован!');
  //console.log('selectedCompanyId:', selectedCompanyId);
  //console.log('selectedHouseId:', selectedHouseId);
});
</script>

<style scoped>

</style>
  