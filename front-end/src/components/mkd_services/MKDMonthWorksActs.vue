<template>
    <div class="mkd-services-year-works-act-wrapper-conteiner">
      <el-row :gutter="20">
        <el-col :span="3">
            <el-date-picker
                v-model="selectedMonthYear"
                type="month"
                placeholder="Месяц и год"
                style="width: 100%"
                value-format="YYYY-MM-DD"
                format="MM-YYYY"
            />
        </el-col>
        <el-col :span="5">
            <el-button type="primary" @click.prevent="generate_month_act" :loading="generateFileInProccess">Сформировать</el-button>
        </el-col>
      </el-row>
      <el-row class="mkd-services-month-year-works-act-row">
        <el-col :span="24">
            <el-table :data="tableData" style="width: 100%" max-height="900" v-loading="tableDataLoading"
            :default-sort="{ prop: 'actYear', order: 'descending' }">
                <el-table-column fixed prop="numOrder" label="№ П/П" width="90" />
                <el-table-column prop="actMonth" label="Месяц" width="100" />
                <el-table-column prop="actYear" label="Год" width="80" sortable />
                <el-table-column prop="actDate" label="Дата акта" width="100" />
                <el-table-column prop="actNum" label="№ Акта" width="140" />
                <el-table-column prop="actFile" label="Наименование" width="320" />
                <el-table-column fixed="right" label="Скачать документ" min-width="120">
                <template #default="scope">
                    <el-button
                    link
                    type="primary"
                    @click.prevent="downloadMonthAct(scope.row.actFileUUID, scope.row.actFile)"
                    >
                    Файл документа
                    </el-button>
                </template>
                </el-table-column>
            </el-table>
        </el-col>
      </el-row>
    </div>
</template>

<script setup>
// Импортируйте необходимые функции, если нужно
import { ref, reactive, computed, onMounted, watch, defineModel, toRaw } from 'vue';
import { get_month_files_list_by_house, generate_month_file_by_house_and_month_and_year, generate_month_file_by_month_and_year,
   get_bg_task_status_by_task_uuid, get_month_act_file_by_uuid, get_month_files_full_list } from '../../http/mkd-works-http-common'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'
import 'dayjs/locale/ru'
dayjs.locale('ru')
import FileDownload from 'js-file-download'

const props = defineProps({
  selectedHouseId: String,
  selectedCompanyId: String,
  selectedHouseName: String,
})
const activeTabMonth = defineModel('activeTabMonth')
const selectedMonthYear = ref('')
const tableData = ref([])
const tableDataLoading = ref(false)
const generateFileInProccess = ref(false)
const bg_year_act_task_id = ref('')
const bg_year_status = ref('')

const downloadMonthAct = (actUUID, filename) =>{
    console.log(actUUID)
    get_month_act_file_by_uuid(actUUID).then((response) => {
      FileDownload(response.data, filename)
    }).catch((error) =>{
      console.error('Error:', error);
    });
}

const showTab = () => {
  console.log(activeTabMonth.value)
}

const statusCheck = async (uuid) => {
  if (uuid) {
    get_bg_task_status_by_task_uuid(uuid).then((response) => {
      console.log(response)
      if (response.status === 200 && response.data["status"] === "done") {
        bg_year_status.value = 'done'
      }
    }).catch((error) => {
      console.error('Error:', error);
    });
  }
  return false
}

/*const refreshTableData = async () => {
  console.log('year act watch', activeTabMonth)
  if (!generateFileInProccess.value) {
    tableDataLoading.value = true
    let refreshData = []
    const response = await get_month_files_list_by_house(props.selectedHouseId);
    for (let [index, element] of response.data.entries()) {
      refreshData.push({
        numOrder: index+1,
        actYear: dayjs(element.year).year(),
        actDate: dayjs(element.date).format('DD.MM.YYYY'),
        actNum: element.num,
        actFile: element.name,
        actFileUUID: element.uuid,
        }
      )
    }
    tableData.value = refreshData
    tableDataLoading.value = false
  }
}*/
const refreshTableData = async () => {
  console.log('month act watch', activeTabMonth);
  if (!generateFileInProccess.value) {
    tableDataLoading.value = true;
    let refreshData = [];
    try {
      if (!props.selectedHouseId) {
        throw new Error('selectedHouseId is not defined');
      }
      //const response = await get_month_files_list_by_house(props.selectedHouseId);
      const response = await get_month_files_full_list()
      if (!response || !response.data) {
        throw new Error('Response is null or does not contain data');
      }
      for (let [index, element] of response.data.entries()) {
        refreshData.push({
          numOrder: index + 1,
          actMonth: dayjs(element.month_year).format('MMMM'),
          actYear: dayjs(element.month_year).format('YYYY'),
          actDate: dayjs(element.date).format('DD.MM.YYYY'),
          actNum: element.num,
          actFile: element.name,
          actFileUUID: element.uuid,
        });
      }
      tableData.value = refreshData;
    } catch (error) {
      console.error('Error in refreshTableData:', error.message);
      ElMessage({
        message: 'Ошибка при загрузке данных: ' + error.message,
        type: 'error',
        showClose: true,
      });
    } finally {
      tableDataLoading.value = false;
    }
  }
};

watch([activeTabMonth, generateFileInProccess], async () => {
  await refreshTableData()
});

watch(() => props.selectedHouseId, (newValue, oldValue) => {
  refreshTableData()
});


function pause(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const generate_month_act = async () => {
  if (!selectedMonthYear.value || !props.selectedHouseId) {
    ElMessage({
        message: 'Выберите месяц и год',
        type: 'warning',
        showClose: true,
    }) 
    return 
  }
  generateFileInProccess.value = true;
  generate_month_file_by_month_and_year(selectedMonthYear.value).then((response) => {
    console.log("RSPONSE BUTTON CLICK", response, response.status, response.data["message"] )
    if (response.status === 200 && response.data["message"] === "task started") {
      bg_year_act_task_id.value = response.data['task_id']
      return
    }else if (response.status === 200 && response.data["message"] === "month act exist") {
      bg_year_status.value = 'create'
      generateFileInProccess.value = false;
      ElMessage({
        message: 'Акт за месяц уже создан',
        type: 'warning',
        showClose: true,
        
      })
      return
    } else if (response.status === 200 && response.data["message"] === "Works not found") {
      generateFileInProccess.value = false;
      ElMessage({
        message: 'За указанный период нет выполненных работ',
        type: 'warning',
        showClose: true,
      })
      return
    }
  }).catch((error) => {
    generateFileInProccess.value = false;
    console.error('Error:', error);
    return
  });
  let count = 0
  if (bg_year_status.value != 'create') {
    for (let i = 0; i < 60; i++) {
      if (bg_year_status.value == 'create' && bg_year_act_task_id.value == '') {
        generateFileInProccess.value = false;
        return
      }
      await statusCheck(bg_year_act_task_id.value);
      count ++;
      if (bg_year_status.value === 'done') {
        ElMessage({
          message: 'Акт за месяц успешно записан',
          type: 'success',
          showClose: true,
        })
        generateFileInProccess.value = false
        return
      }
      
      console.log('COUNT', count)
      await pause(1000);
    }
    bg_year_status.value = ''
  } 
  bg_year_status.value = ''
}


onMounted(() => {
  console.log('Компонент был смонтирован!');
  
});
</script>

<style scoped>
.mkd-services-month-year-works-act-row {
  margin-top: 1em;
}
</style>
  