<template>
    <div class="mkd-services-works-regester-wrapper-conteiner">
      <!--<el-text class="mx-1" size="large">{{ selectedCompanyId }} - {{ selectedHouseId }}</el-text>-->
      <el-table :data="tableData" style="width: 100%" max-height="900" v-loading="loading">
        <el-table-column fixed prop="numOrder" label="№" width="50" />
        <el-table-column fixed prop="numSprav" label="Разд. Справ." width="69" />
        <el-table-column label="Наименование работы" width="500">
          <template #default="scope">
            <span class="mkd-service-cell_text " :title="scope.row.work">{{ scope.row.work }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="smeta.date" label="Дата сметы" width="100" :formatter="dateFromDB" />
        <el-table-column prop="numSmeta" label="№ Сметы / Файл" width="140">
          <template #default="scope">
            <div style="display: flex; align-items: center">
              <span>{{ scope.row.smeta.num }}</span>
              <span style="margin-left: 10px; margin-bottom: 0.2em;">
                <el-link type="success" :underline="false" v-if="scope.row.smeta.url" @click.prevent="downloadFile(scope.row.smeta.url + scope.row.smeta.uuid, scope.row.smeta.name)">Файл Сметы</el-link>
              </span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="act.date" label="Дата акта" width="100" :formatter="dateFromDB" />
        <el-table-column prop="act.num" label="№ Акта / Файл" width="140">
          <template #default="scope">
            <div style="display: flex; align-items: center">
              <span>{{ scope.row.act.num }}</span>
              <span style="margin-left: 10px; margin-bottom: 0.2em;">
                <el-link type="success" :underline="false" v-if="scope.row.act.url" @click.prevent="downloadFile(scope.row.smeta.url + scope.row.smeta.uuid, scope.row.smeta.name)">Файл Акта</el-link>
              </span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="monthWork" label="Месяц пров. работ" width="100" :formatter="monthWorkFromDB" />
        <el-table-column prop="yearWork" label="Год пров. работ" width="100" :formatter="yearWorkFromDB"/>
        <el-table-column prop="sumWork" label="Стоимость работ" width="100" :formatter="formatToDecimal"/>
        <el-table-column fixed="right" label="Редактирование" min-width="120">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="small"
              @click.prevent="EditRow(scope.$index)"
            >
              редактировать
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-button class="mt-4" style="width: 100%" @click="onAddItem">
        Добавить сведения об услуге/работе
      </el-button>
      <MKDWorkAddModal 
        v-model:dialogMKDWorksAddVisibleSub="showMKDWorkAddModal"
        v-model:workFromDBdata="workFromDBdataMain"
        :house-id="props.selectedHouseId" 
        :company="props.selectedCompanyId"
        :house-name="props.selectedHouseName"
        :work-ID="workID"
        :all-works-options="props.allWorksRef"
        :all-periods-options="props.worksPeriodsRef"
        :modal-call-type="modalCallType"
        :edit-row-index="editRowIndex"
        @update-data="updateTableData"
        />
    </div>
</template>

<script setup>
// Импортируйте необходимые функции, если нужно
import { ref, reactive, computed, onMounted, watch, defineModel, toRaw } from 'vue';
import MKDWorkAddModal from './modal/MKDWorkAddModal.vue';
import { get_mkd_works_get_all_works_by_house_id, download_file_mkd_works } from '../../http/mkd-works-http-common'
import { mkd_works_works_to_string, get_mkd_works_sprav_name, get_period } from '../../utils/utils'
import dayjs from 'dayjs';
import FileDownload from 'js-file-download'
import { configProviderContextKey } from 'element-plus';

const props = defineProps({
  selectedHouseId: String,
  selectedCompanyId: String,
  selectedHouseName: String,
  allWorksRef: Array,
  worksPeriodsRef: Array,
})
const months =["Январь", "Февраль", "Март", "Апрель", "Mай", "Июнь", "Июль",
    "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
  ]
const showMKDWorkAddModal = ref(false)
const workID =ref('')
const workFromDBdataMain = ref(null)
const loading = ref(true)
const modalCallType=ref('add')
const editRowIndex = ref(null)
const tableData = ref([])

const formatToDecimal = (row, column, cellValue, index) => {
    // Если строка пустая или не определена, возвращаем "0.00"
    if (!cellValue || cellValue.trim() === '') {
        return '0.00';
    }
    // Заменяем запятые на точки
    cellValue = cellValue.replace(/,/g, '.');
    // Проверяем, есть ли в строке точка
    if (!cellValue.includes('.')) {
        // Если точки нет, добавляем ".00" в конец строки
        cellValue += '.00';
    } else {
        // Если точка есть, проверяем количество знаков после нее
        const [integerPart, decimalPart] = cellValue.split('.');
        // Обрезаем или дополняем дробную часть до двух знаков
        cellValue = `${integerPart}.${(decimalPart || '').padEnd(2, '0').slice(0, 2)}`;
    }
    return cellValue;
}

const EditRow = (index) => {
  //tableData.value.splice(index, 1)
  console.log("Asdasdasd", modalCallType.value)
  modalCallType.value = 'edit'
  console.log("Asdasdasd", modalCallType.value)
  showMKDWorkAddModal.value = true
  editRowIndex.value = index
  workFromDBdataMain.value = tableData.value[index]
  //console.log("dddddddddddddddddddddddddddddddddd", tableData.value[index].workId)
  workID.value = String(tableData.value[index].workId)
}

const onAddItem = () => {
  if (!props.selectedHouseId) {
    return
  }
  showMKDWorkAddModal.value = true
  workID.value = ''
  modalCallType.value = 'add'
  editRowIndex.value = null
  workFromDBdataMain.value = initEmptyRowData()
}

const dateFromDB = function (row, column, cellValue, index) {
  console.log('DATE', cellValue)
  if (cellValue)
    return dayjs(cellValue).format('DD.MM.YYYY')
  else
    return ''
}

const monthWorkFromDB = function (row, column, cellValue, index) {
  console.log(cellValue, '----------------------')
  if (cellValue)
    return months[dayjs(cellValue).month()]
  else
    return ''
}

const yearWorkFromDB = function (row, column, cellValue, index) {
  if (cellValue)
    return dayjs(cellValue).year()
  else
    return ''
}


const worksDataFromDBtoTableView = (worksData) => {
  for (let [index, element] of worksData.entries()) {
    tableData.value.push({
      numOrder: index + 1,
      numSprav: element.num ? element.num : get_mkd_works_sprav_name(element.mainworks, element.subworks, element.fixworks),
      work: mkd_works_works_to_string(element.mainworks, element.subworks, element.fixworks),
      smeta: element.smetafiles.length > 0 ? element.smetafiles[0]: {num: '', url: '', date: '', uuid: '', name: ''},
      act: element.actfiles.length  > 0 ? element.actfiles[0]: {num: '', url: '', date: '', uuid: '', name: ''},
      period: get_period(element.subworks, element.fixworks),
      monthWork: element.month_year_works,
      yearWork: element.month_year_works,
      sumWork: element.all_sum,
      quantSum: element.unit_cost,
      squareWork: element.work_square,
      workId: element.id,
      mainWorkId: '',
      subWorkId: '',
      fixWorkId: '',
      dirFIO: element.director,
      dirAppart: element.director_appartment,
      mainworks: element.mainworks,
      subworks: element.subworks,
      fixworks: element.fixworks,
    })
  }
  //console.log("asddddddddddddd", tableData.value)
}

const updateTableData = () => {
  loading.value = true
  get_mkd_works_get_all_works_by_house_id(props.selectedHouseId).then((response) => {
    tableData.value = []
    worksDataFromDBtoTableView(response.data)
    loading.value = false
  }).catch((error) => {
    console.error('Error:', error);
  });
}

watch(() => props.selectedHouseId, (newSelectedHouseId, oldSelectedHouseId) => {
  console.log("newProps", newSelectedHouseId, oldSelectedHouseId)
  console.log(props.selectedHouseName)
  loading.value = true
  get_mkd_works_get_all_works_by_house_id(newSelectedHouseId).then((response) => {
    tableData.value = []
    worksDataFromDBtoTableView(response.data)
    loading.value = false
  }).catch((error) => {
    console.error('Error:', error);
  });
})

const initEmptyRowData = () => {
  return {
    numOrder: null,
    numSprav: '',
    work: '',
    smeta: {num: '', url: '', date: '', uuid: '', name: ''},
    act: {num: '', url: '', date: '', uuid: '', name: ''},
    monthWork: '',
    yearWork: '',
    sumWork: '',
    workId: '',
    mainWorkId: '',
    subWorkId: '',
    fixWorkId: '',
  }
}

const downloadFile = (url, filename) => {
  download_file_mkd_works(url).then((response) =>{
    FileDownload(response.data, filename)
  }).catch((error) =>{
    console.error('Error:', error);
  });
}


onMounted(() => {
  console.log('Компонент был смонтирован!');
  console.log('props!', props.selectedHouseId);
  get_mkd_works_get_all_works_by_house_id(props.selectedHouseId).then((response) => {
    worksDataFromDBtoTableView(response.data)
    workFromDBdataMain.value = initEmptyRowData()
    loading.value = false
  }).catch((error) => {
    console.error('Error:', error);
  });
  //console.log('selectedCompanyId:', selectedCompanyId);
  //console.log('selectedHouseId:', selectedHouseId);
});
</script>

<style scoped>
.mkd-service-cell_text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
  