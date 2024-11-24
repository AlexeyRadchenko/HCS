<template>
    <div class="mkd-photo-fix-works-wrapper-conteiner">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-upload
            ref="techFile"
            :data="getPhotoWorksData"
            class="upload-demo"
            :action="api_main_url_port + '/api/v1/mkd_works_service/uploadfile/photofixwork'"
            :limit="1"
            :on-exceed="handleExceedTechFiles"
            :on-success="uploadTechFileSuccess"
            :headers="uploadHeaders"
            :auto-upload="false"
            :disabled="techFileUploadBtnDisabled"
          >
            <template #trigger>
              <el-button type="primary">Выберите файл</el-button>
            </template>
            <el-button class="mkd-service-tech-tab-btnml" type="success" @click="submitTechFileUpload">
              Загрузить на сервер
            </el-button>
            <template #tip>
              <div class="el-upload__tip text-red">
                ограничение 1 файл, старый файл перезапишется новым
              </div>
            </template>
          </el-upload>
        </el-col>
        <el-col :span="3">
          <el-date-picker
            v-model="inpudDataTechDoc.dateFile"
            type="date"
            format="DD.MM.YYYY"
            placeholder="Дата документа"
            style="width: 100%"
            value-format="YYYY-MM-DD"
          />
        </el-col>
        <el-col :span="3">
          <el-input
            v-model="inpudDataTechDoc.numFile"
            style="width: 100%;"
            placeholder="Номер документа"
            clearable
          />
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
            <el-table :data="tableData" style="width: 100%" max-height="900" v-loading="tableTechDocDataLoading">
                <el-table-column fixed prop="techFileNumOrder" label="№ П/П" width="90" />
                <el-table-column prop="techFileYear" label="Год" width="100" />
                <el-table-column prop="techFileDate" label="Дата документа" width="100" />
                <el-table-column prop="techFileNum" label="№ док-та" width="140" />
                <el-table-column prop="techFileName" label="Нименование док-та" width="320" />
                <el-table-column fixed="right" label="Файл" min-width="120">
                <template #default="scope">
                    <el-button
                    link
                    type="primary"
                    @click.prevent="showActData(scope.row.uuid)"
                    >
                    Скачать
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
import secureStorage from '../../storage/secStorage'
import { genFileId, ElMessage } from 'element-plus'
import { get_techdoc_files_list_by_house } from '../../http/mkd-works-http-common'
import dayjs from 'dayjs'

const props = defineProps({
  selectedHouseId: String,
  selectedCompanyId: String,
  selectedHouseName: String,
})
const api_main_url_port = ref('')
const activeTabTechDoc = defineModel("activeTabTechDoc")
const techFileUploadBtnDisabled = ref(false)
const techFile = ref(null)
const inpudDataTechDoc = ref({
  dateFile: '',
  numFile: ''
})
const tableData = ref([])
const tableTechDocDataLoading = ref(false)

//upload files methods
const uploadHeaders = {
  'Authorization': 'Bearer ' + secureStorage.getItem('token')
}

const getPhotoWorksData = () => {
  return {
    docnum: inpudDataTechDoc.value.numFile, // любые ваши данные
    docdate: inpudDataTechDoc.value.dateFile,
    houseid: props.selectedHouseId
  }
}

const handleExceedTechFiles = (files) => { 
  if (techFile.value) {
    techFile.value.clearFiles()
  }
  const file = files[0]
  console.log(file)
  file.uid = genFileId()
  console.log(file)
  if (techFile.value) {
    techFile.value.handleStart(file)
  }
}


const submitTechFileUpload = () => {
  if (techFile.value) {
    techFileUploadBtnDisabled.value = true
    techFile.value.submit()
  }
  
}

const uploadTechFileSuccess = (response) => {
    let order = tableData.value.length
    tableData.push({
      techFileNumOrder: order + 1,
      techFileYear: response.techfiledate ? dayjs(response.techfiledate).year() : '',
      techFileDate: response.techfiledate ? dayjs(response.techfiledate).format('DD.MM.YYYY') : '',
      techFileNum: response.techfilenum ? response.techfilenum : '',
      techFileName:  response.techfilename,
      uuid: response.uuid,
    })
    techFileUploadBtnDisabled.value = false
    ElMessage({
      showClose: true,
      message: 'Файл успешно загружен',
      type: 'success',
    })
}

const refreshTechTableData = async() => {
  console.log('TECHTAB', activeTabTechDoc.value, techFileUploadBtnDisabled.value)
  if (!techFileUploadBtnDisabled.value) {
    tableTechDocDataLoading.value = true
    let refreshData = []
    const response = await get_techdoc_files_list_by_house(props.selectedHouseId);
    for (let [index, element] of response.data.entries()) {
      refreshData.push({
        techFileNumOrder: index+1,
        techFileYear: dayjs(element.date).year(),
        techFileDate: dayjs(element.date).format('DD.MM.YYYY'),
        techFileNum: element.num,
        techFileName: element.name,
        uuid: element.uuid,
        }
      )
    }
    tableData.value = refreshData
    tableTechDocDataLoading.value = false
  }
}

watch([activeTabTechDoc, techFileUploadBtnDisabled], async () => {
  await refreshTechTableData()
});

watch(() => props.selectedHouseId, (newValue, oldValue) => {
  refreshTechTableData()
});


onMounted(() => {
  console.log('Компонент был смонтирован!');
  api_main_url_port.value = import.meta.env.VITE_API_BASEURL;

  if (import.meta.env.VITE_API_BASEPORT) {
    api_main_url_port.value = `${api_main_url_port}:${import.meta.env.VITE_API_BASEPORT}`;
  }
  //console.log('selectedCompanyId:', selectedCompanyId);
  //console.log('selectedHouseId:', selectedHouseId);
});
</script>

<style scoped>
.mkd-service-tech-tab-btnml {
  margin-left: 1em;
}
</style>
