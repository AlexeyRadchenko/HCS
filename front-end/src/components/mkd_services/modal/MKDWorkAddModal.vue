
<template>
    <div class="mkd-works-add-modal-wrapper-conteiner">
        <el-dialog v-model="dialogMKDWorksAddVisibleSub" :title="'Добавление/Редактирование сведений о работах по МКД '+ houseName" width="1250">
          <el-container>
            <main style="width: 100%;">
                <el-row :gutter="20">   
                    <el-col :span="12">
                        <el-text class="mx-1" size="large">Приложить файл сметы</el-text>
                    </el-col>
                    <el-col :span="12">
                        <el-text class="mx-1" size="large">Сведения для составления акта</el-text>
                    </el-col>
                </el-row>
                <el-row class="file-inout-row-cl" :gutter="20">
                    <el-col :span="3">
                      <el-input
                        v-model="smetaInputFileData.smetanum"
                        style="width: 100%"
                        placeholder="Номер сметы"
                        clearable
                      />
                    </el-col>
                    <el-col :span="3">
                      <el-date-picker
                        v-model="smetaInputFileData.smetadate"
                        type="date"
                        format="DD.MM.YYYY"
                        placeholder="Дата сметы"
                        style="width: 100%"
                        value-format="YYYY-MM-DD"
                      />
                    </el-col>
                    <el-col :span="5">
                        <el-upload
                            ref="uploadSmeta"
                            :data="getDataSmetaFile"
                            action="http://localhost:8050/api/v1/mkd_works_service/uploadfile/smeta"
                            :limit="1"
                            :on-exceed="handleExceedSmeta"
                            :auto-upload="false"
                            :headers="uploadHeaders"
                            :on-success="uploadSmetaSuccess"
                        >
                            <template #trigger>
                            <el-button type="primary">select file</el-button>
                            </template>
                            <el-button style="margin-left: 1em;" type="success" @click="submitUploadSmeta">
                            Загрузить
                            </el-button>
                            <template #tip>
                            <div class="el-upload__tip text-red">
                                ограничение 1 файл, файл можно перезаписать новым
                            </div>
                            </template>
                        </el-upload>
                    </el-col>
                    <el-col :span="9">
                      <el-input
                        v-model="workInputData.directorSovietFIO"
                        style="width: 100%"
                        placeholder="ФИО председателя совета дома, например Иванов И.И."
                        clearable
                      />
                    </el-col>
                    <el-col :span="3">
                      <el-input
                        v-model="workInputData.directorAppartNum"
                        style="width: 100%"
                        placeholder="Номер квартиры"
                        clearable
                      />
                    </el-col>
                </el-row>
                <el-row :gutter="20">   
                    <el-col :span="11">
                        <el-text class="mx-1" size="large">Приложить файл акта</el-text>
                    </el-col>
                    <el-col :span="6">
                      <el-date-picker
                        v-model="workInputData.workMonthAndYear"
                        type="month"
                        format="MM.YYYY"
                        placeholder="Месяц и год проведения работ"
                        style="width: 100%"
                        value-format="YYYY-MM-DD"
                      />
                    </el-col>
                    <el-col :span="6">
                      <el-input
                        v-model="workInputData.actAllSumHandle"
                        style="width: 100%"
                        placeholder="Общая сумма"
                        clearable
                      />
                    </el-col>
                </el-row>
                <el-row class="file-inout-row-cl" :gutter="20">
                  <el-col :span="3">
                    <el-input
                      v-model="actInputFileData.actnum"
                      style="width: 100%"
                      placeholder="Номер Акта"
                      clearable
                    />
                  </el-col>
                  <el-col :span="3">
                    <el-date-picker
                        v-model="actInputFileData.actdate"
                        type="date"
                        format="DD.MM.YYYY"
                        style="width: 100%"
                        placeholder="Дата акта"
                        value-format="YYYY-MM-DD"
                      />
                  </el-col>
                  <el-col :span="5">
                      <el-upload
                          ref="uploadAct"
                          :data="getDataActFile"
                          action="http://localhost:8050/api/v1/mkd_works_service/uploadfile/act"
                          :limit="1"
                          :on-exceed="handleExceedAct"
                          :auto-upload="false"
                          :headers="uploadHeaders"
                          :on-success="uploadActSuccess"
                      >
                          <template #trigger>
                          <el-button type="primary">select file</el-button>
                          </template>
                          <el-button style="margin-left: 1em;" type="success" @click="submitUploadAct">
                          Загрузить
                          </el-button>
                          <template #tip>
                          <div class="el-upload__tip text-red">
                              ограничение 1 файл, файл можно перезаписать новым
                          </div>
                          </template>
                      </el-upload>
                  </el-col>
                  <el-col :span="12">
                    <el-text size="large">Прикрепленные документы:</el-text>
                    <el-row :gutter="20" class="mkd-works-apply-docs-margin">
                    <el-col :span="24">
                      <el-row :gutter="20">
                        <el-col :span="5">{{ actDownloadFile.date }}</el-col>
                        <el-col :span="19"><el-link :href="actDownloadFile.url + actDownloadFile.uuid">{{ actDownloadFile.filename }}</el-link></el-col>
                      </el-row>
                      <el-row :gutter="20" class="mkd-works-apply-docs-margin">
                        <el-col :span="5">{{ smetaDowmloadFile.date }}</el-col>
                        <el-col :span="19"><el-link :href="smetaDowmloadFile.url + smetaDowmloadFile.uuid">{{ smetaDowmloadFile.filename }}</el-link></el-col>
                      </el-row>
                    </el-col>     
                </el-row>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="24">
                    <el-table :data="tableData" style="width: 100%" max-height="450">
                      <el-table-column label="№ П/П" width="65">
                        <template #default="scope">
                          <el-input v-model="scope.row.orderNum" style="width: 100%"/>
                        </template>
                      </el-table-column>
                      <el-table-column label="Разд. справ." width="80">
                        <template #default="scope">
                          <el-input v-model="scope.row.numsprav" style="width: 100%"/>
                        </template>
                      </el-table-column>
                      <el-table-column  label="Наименование вида работы (услуги)" width="420">
                        <template #default="scope">
                          <el-select-v2
                            v-model="scope.row.nameWorkOrService"
                            :options="allWorksOptions"
                            placeholder="Выберите работу услугу"
                            style="width: 100%"
                            filterable
                            clearable
                          />
                        </template>
                      </el-table-column>  
                      <el-table-column label="Периодичость" width="200">
                        <template #default="scope">
                          <el-select-v2
                            v-model="scope.row.period"
                            :options="allPeriodsOptions"
                            placeholder="Периодичность"
                            style="width: 100%"
                            filterable
                            clearable
                          />
                        </template>
                      </el-table-column>
                      <el-table-column label="Кол-во единиц измерений" width="80">
                        <template #default="scope">
                          <el-input v-model="scope.row.quantity" style="width: 100%"/>
                        </template>
                      </el-table-column>
                      <el-table-column label="Стоимость оказанной услуги за единицу, руб/м2" width="120">
                        <template #default="scope">
                          <el-input v-model="scope.row.costOfPart" style="width: 100%"/>
                        </template>
                      </el-table-column>
                      <el-table-column label="Цена выполненной работы (оказанной услуги) в рублях" width="120">
                        <template #default="scope">
                          <el-input v-model="scope.row.sum" style="width: 100%"/>
                        </template>
                      </el-table-column>
                      <el-table-column fixed="right" label="Строка" min-width="35">
                        <template #default="scope">
                          <el-button
                            link
                            type="danger"
                            size="small"
                            @click.prevent="deleteRow(scope.$index)"
                          >
                            Удалить
                          </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                    <el-button class="mt-4" style="width: 100%" @click="onAddItem">
                      Добавить строку
                    </el-button>
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="5">
                    <el-button type="primary" style="width: 100%" @click="onSaveBtnClick">Сохранить</el-button>
                  </el-col>
                  <el-col :span="3" class="mkd-works-left-margin-col">
                    <el-button type="info" style="width: 100%">Отменить</el-button>
                  </el-col>
                </el-row>
            </main>  
          </el-container>
        </el-dialog>
    </div>
</template>

<script setup>
// Импортируйте необходимые функции, если нужно
import { ref, reactive, computed, onMounted, watch, toRaw } from 'vue';
import { genFileId } from 'element-plus'
import secureStorage from '../../../storage/secStorage'
import { get_future_work_id_by_house_id } from '../../../http/mkd-works-http-common'
import dayjs from 'dayjs'
import { all } from 'axios';


const props = defineProps({
    houseId: String,
    company: String,
    houseName: String,
    workID: String,
    modalCallType: String,
    allWorksOptions: Array,
    allPeriodsOptions: Array,
    editRowIndex: Number,
})
//{1}_2_{2} или {1}_1_{2} перваое это mainworkid, один или два -> тип работы sub илил fix, последнее id работы
const uploadHeaders = {
  'Authorization': 'Bearer ' + secureStorage.getItem('token')
}

const dialogMKDWorksAddVisibleSub = defineModel('dialogMKDWorksAddVisibleSub')
const workFromDBdata = defineModel('workFromDBdata')
const uploadSmeta = ref(null)
const uploadAct = ref(null)
const workInputData = ref({
  workMonthAndYear: '',
  actAllSumHandle: '',
  directorSovietFIO: '',
  directorAppartNum: '',
})
const actInputFileData = ref({
  actnum: '',
  actdate: '',
  actfutureid: null,
  workid: null,
  houseid: props.houseId,
})

const actDownloadFile = ref({
  filename: '',
  url: '',
  date: '',
  num: '',
  uuid: '',
  workid: ''
})

const smetaInputFileData = ref({
  smetanum: '',
  smetadate: '',
  actfutureid: null,
  workid: null,
  houseid: props.houseId,
})

const smetaDowmloadFile = ref({
  filename: '',
  url: '',
  date: '',
  num: '',
  uuid: '',
  workid: ''
})

const getDataActFile = () => {
  console.log("sibdataloading", actInputFileData.value)
  return {
    actnum: actInputFileData.value.actnum, // любые ваши данные
    actdate: actInputFileData.value.actdate,
    workid: props.workID,
    houseid: props.houseId
  };
};

const getDataSmetaFile = () => {
  return {
    smetanum: smetaInputFileData.value.smetanum, // любые ваши данные
    smetadate: smetaInputFileData.value.smetadate,
    workid: props.workID,
    houseid: props.houseId
  };
}    
const uploadActSuccess = (response) => {
    console.log(response)
    actDownloadFile.value.filename = response.filename
    actDownloadFile.value.date = response.actdate ? dayjs(response.actdate).format('DD.MM.YYYY') : ''
    actDownloadFile.value.num = response.actnum
    actDownloadFile.value.workid = response.workid
    if (!workFromDBdata.value.workId) {
      workFromDBdata.value.workId = response.workid
    }
}

const uploadSmetaSuccess = (response) => {
    console.log(response)
    smetaDowmloadFile.value.filename = response.filename
    smetaDowmloadFile.value.date = response.smetadate ? dayjs(response.smetadate).format('DD.MM.YYYY') : ''
    smetaDowmloadFile.value.num = response.smetanum,
    smetaDowmloadFile.value.workid = response.workid
    if (!workFromDBdata.value.workId) {
      workFromDBdata.value.workId = response.workid
    }
}

watch(() => props.dialogMKDWorksAddVisibleSub, (show, oldStatus) => {
  console.log(show, oldStatus)
  if (show && props.modalCallType == 'edit') {
    console.log(props.modalCallType, props.editRowIndex)
    console.log(workFromDBdata.value)
    console.log("!!!!!!!!!!!!!!!!!!!!!!!!!",props.houseId, props.workID)
    actInputFileData.value.workid = workFromDBdata.value.workId
    smetaInputFileData.value.workid = workFromDBdata.value.workId
    workInputData.value.workMonthAndYear = dayjs(workFromDBdata.value.date).format('YYYY-MM-DD')
    workInputData.value.directorSovietFIO = workFromDBdata.value.dirFIO
    workInputData.value.directorAppartNum = workFromDBdata.value.dirAppart
    workInputData.value.actAllSumHandle = workFromDBdata.value.sumWork
    actDownloadFile.value.num = workFromDBdata.value.act.num
    actDownloadFile.value.date = workFromDBdata.value.act.date ? dayjs(workFromDBdata.value.act.date).format('DD.MM.YYYY') : ''
    actDownloadFile.value.url = workFromDBdata.value.act.url
    actDownloadFile.value.uuid = workFromDBdata.value.act.uuid
    actDownloadFile.value.workid = workFromDBdata.value.workId
    actDownloadFile.value.filename= workFromDBdata.value.act.name
    smetaDowmloadFile.value.num = workFromDBdata.value.smeta.num
    smetaDowmloadFile.value.date = workFromDBdata.value.smeta.date ? dayjs(workFromDBdata.value.smeta.date).format('DD.MM.YYYY') : ''
    smetaDowmloadFile.value.url = workFromDBdata.value.smeta.url
    smetaDowmloadFile.value.uuid = workFromDBdata.value.smeta.uuid
    smetaDowmloadFile.value.workid = workFromDBdata.value.smeta.workId
    smetaDowmloadFile.value.filename = workFromDBdata.value.smeta.name
    tableData.value[0].numsprav = workFromDBdata.value.numSprav
    tableData.value[0].nameWorkOrService = workFromDBdata.value.work
    tableData.value[0].period = workFromDBdata.value.period
    tableData.value[0].quantity = workFromDBdata.value.quaquantSum
    tableData.value[0].costOfPart = workFromDBdata.value.squareWork
    tableData.value[0].sum = workFromDBdata.value.sumWork
  }
  //console.log(workInputData.value.workMonthAndYear, dayjs(workFromDBdata.value.date).format('MM.YYYY'))
})



//upload files methods
const handleExceedSmeta = (files) => { 
  console.log("!smeta")
  if (uploadSmeta.value) {
    uploadSmeta.value.clearFiles()
  }
  const file = files[0]
  console.log(file)
  file.uid = genFileId()
  console.log(file)
  if (uploadSmeta.value) {
    uploadSmeta.value.handleStart(file)
  }
}

const submitUploadSmeta = () => {
  if (uploadSmeta.value) {
    uploadSmeta.value.submit()
  }
}

const handleExceedAct = (files) => { 
  console.log("!act", uploadAct.value)
  if (uploadAct.value) {
    uploadAct.value.clearFiles()
  }
  const file = files[0]
  console.log(file)
  file.uid = genFileId()
  if (uploadAct.value) {
    uploadAct.value.handleStart(file)
  }
}

const submitUploadAct = () => {
  if (uploadAct.value) {
    uploadAct.value.submit()
  }
}

const tableData = ref([
  {
    orderNum: 1,
    numsprav: '',
    nameWorkOrService: '',
    period: '',
    quantity: '',
    costOfPart: '',
    sum: '0.00',
  },
])

const deleteRow = (index) => {
  tableData.value.splice(index, 1)
}

const onAddItem = () => {
  tableData.value.push({
    orderNum: tableData.value.length + 1,
    nameWorkOrService: '',
    period: '',
    quantity: '',
    costOfPart: '',
    sum: '0.00',
  })
}

const onSaveBtnClick = () => {
  console.log(props.modalCallType)
}

/*const work_id_from_db = (houseID) => {
  get_future_work_id_by_house_id(houseID).then((response) => {
    tempWorkFutureId.value = response.data.future_work_id
    actInputFileData.value.actfutureid = response.data.future_work_id
    console.log("work id future", tempWorkFutureId.value)
  }).catch((error) => {
    console.error('Error:', error);
  });
}

watch(dialogMKDWorksAddVisibleSub, (dialogMKDWorksAddVisibleSub) => {
  if (dialogMKDWorksAddVisibleSub && !props.workID) {
    work_id_from_db(props.houseId)
  }else if (props.workID) {
    actInputFileData.value.actfutureid = props.workID
  }
})*/ 

//watch(() => props.selectedHouseId, (newSelectedHouseId, oldSelectedHouseId) => {

onMounted(() => {
  console.log('Компонент был смонтирован!');
});
</script>

<style scoped>
.file-inout-row-cl {
  margin-top: 1em;
}
.mkd-works-left-margin-col {
  margin-left: 1em;
}
.mkd-works-apply-docs-margin {
  margin-top: 1em
}
</style>