
<template>
    <div class="mkd-works-add-modal-wrapper-conteiner">
        <el-dialog v-model="dialogMKDWorksAddVisibleSub" :title="'Добавление/Редактирование сведений о работах по МКД '+ props.houseName" width="1250">
          <el-container>
            <main style="width: 100%;">
                <el-row>   
                    <el-col :span="12">
                        <el-text class="mx-1" size="large">Приложить файл сметы</el-text>
                    </el-col>
                    <el-col :span="12">
                        <el-text class="mx-1" size="large">Сведения для составления акта</el-text>
                    </el-col>
                </el-row>
                <el-row class="file-inout-row-cl">
                    <el-col :span="4">
                      <el-input
                        v-model="inputSmetaNum"
                        style="width: 12em"
                        placeholder="Введите номер сметы"
                        clearable
                      />
                    </el-col>
                    <el-col :span="7">
                        <el-upload
                            ref="uploadSmeta"
                            action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
                            :limit="1"
                            :on-exceed="handleExceedSmeta"
                            :auto-upload="false"
                        >
                            <template #trigger>
                            <el-button type="primary">select file</el-button>
                            </template>
                            <el-button style="margin-left: 1em;" type="success" @click="submitUploadSmeta">
                            upload to server
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
                        v-model="actInputData.directorSovietFIO"
                        style="width: 100%"
                        placeholder="ФИО председателя совета дома, например Иванов И.И."
                        clearable
                      />
                    </el-col>
                    <el-col :span="3" class="mkd-works-left-margin-col">
                      <el-input
                        v-model="actInputData.directorAppartNum"
                        style="width: 100%"
                        placeholder="Номер квартиры"
                        clearable
                      />
                    </el-col>
                </el-row>
                <el-row>   
                    <el-col :span="11">
                        <el-text class="mx-1" size="large">Приложить файл акта</el-text>
                    </el-col>
                    <el-col :span="5">
                      <el-date-picker
                        v-model="actInputData.actDate"
                        type="date"
                        format="DD.MM.YYYY"
                        placeholder="Дата составления акта"
                        :size="size"
                        style="width: 100%"
                      />
                    </el-col>
                    <el-col :span="7" class="mkd-works-left-margin-col">
                      <el-date-picker
                        v-model="actInputData.actPeriod"
                        type="daterange"
                        range-separator="до"
                        start-placeholder="Дата нач. работ"
                        end-placeholder="Дата окон. работ"
                        forma="DD.MM.YYYY"
                        style="width: 100%"
                      />
                    </el-col>
                </el-row>
                <el-row class="file-inout-row-cl">
                  <el-col :span="4">
                      <el-input
                        v-model="inputActNum"
                        style="width: 12em"
                        placeholder="Введите номер Акта"
                        clearable
                      />
                    </el-col>
                    <el-col :span="7">
                        <el-upload
                            ref="uploadSmeta"
                            action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
                            :limit="1"
                            :on-exceed="handleExceedAct"
                            :auto-upload="false"
                        >
                            <template #trigger>
                            <el-button type="primary">select file</el-button>
                            </template>
                            <el-button style="margin-left: 1em;" type="success" @click="submitUploadAct">
                            upload to server
                            </el-button>
                            <template #tip>
                            <div class="el-upload__tip text-red">
                                ограничение 1 файл, файл можно перезаписать новым
                            </div>
                            </template>
                        </el-upload>
                    </el-col>
                    <el-col :span="5">
                      <el-input
                        v-model="actInputData.actAllSumHandle"
                        style="width: 100%; margin-top: 1em;"
                        placeholder="Общая сумма"
                        clearable
                      />
                    </el-col>
                    <el-col :span="3" class="mkd-works-left-margin-col">
                      <el-button type="primary" style="width: 100%; margin-top: 1em;">Сохранить</el-button>
                    </el-col>
                </el-row>
                <el-row>
                  <el-col :span="24">
                    <el-table :data="tableData" style="width: 100%" max-height="450">
                      <el-table-column label="№ П/П" width="90">
                        <template #default="scope">
                          <el-input v-model="scope.row.orderNum" style="width: 100%"/>
                        </template>
                      </el-table-column>
                      <el-table-column  label="Наименование вида работы (услуги)" width="420">
                        <template #default="scope">
                          <el-select-v2
                            v-model="scope.row.nameWorkOrService"
                            :options="works"
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
                            :options="periods"
                            placeholder="Периодичность"
                            style="width: 100%"
                            filterable
                            clearable
                          />
                        </template>
                      </el-table-column>
                      <el-table-column label="Кол-во единиц измерений" width="120">
                        <template #default="scope">
                          <el-input v-model="scope.row.quantity" style="width: 100%"/>
                        </template>
                      </el-table-column>
                      <el-table-column label="Стоимость оказанной услуги за единицу, руб/м2" width="130">
                        <template #default="scope">
                          <el-input v-model="scope.row.costOfPart" style="width: 100%"/>
                        </template>
                      </el-table-column>
                      <el-table-column label="Цена выполненной работы (оказанной услуги) в рублях" width="170">
                        <template #default="scope">
                          <el-input v-model="scope.row.Sum" style="width: 100%"/>
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
                            Remove
                          </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                    <el-button class="mt-4" style="width: 100%" @click="onAddItem">
                      Add Item
                    </el-button>
                  </el-col>
                </el-row>
            </main>  
          </el-container>
        </el-dialog>
    </div>
</template>

<script setup>
// Импортируйте необходимые функции, если нужно
import { ref, reactive, computed, onMounted, watch, defineModel, toRaw, defineProps } from 'vue';
import { genFileId } from 'element-plus'
import dayjs from 'dayjs'


const props = defineProps({
    houseId: String,
    company: String,
    houseName: String,
})

const dialogMKDWorksAddVisibleSub = defineModel('dialogMKDWorksAddVisibleSub')
const uploadSmeta = ref(null)
const uploadAct = ref(null)
const actInputData = ref({
  actNum: '',
  actDate: '',
  actPeriod: '',
  actAllSumHandle: '',
  directorSovietFIO: '',
  directorAppartNum: '',
})
const inputSmetaNum = ref('')
const inputActNum = ref('')
const worksNames = ['JDkjfglasfld', 'adsasdasdads', 'KGFgkl;ldskfgldkfgdfgsdfsdfsdfgsfgdfgdlbkjdlbgkjdlkhbgjdlkfjgldkfjg', 'fsjkgvlskgjldsfk', 'e', 'f', 'g', 'h', 'i', 'j']
const periodsNames = ['постоянно', '6 месяцев', 'согласно санитарным нормам',]

const works = Array.from({ length: worksNames.length}).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: worksNames[idx],
}))

const periods = Array.from({ length: periodsNames.length}).map((_, idx) => ({
  value: `Option ${idx + 1}`,
  label: periodsNames[idx],
}))


const handleExceedSmeta = (files) => { 
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
  if (uploadAct.value) {
    uploadAct.value.clearFiles()
  }
  const file = files[0]
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
    orderNum: '1',
    nameWorkOrService: 'Tom',
    period: 'California',
    quantity: 'Los Angeles',
    costOfPart: 'No. 189, Grove St, Los Angeles',
    Sum: 'CA 90036',
  },
])

const deleteRow = (index) => {
  tableData.value.splice(index, 1)
}

const onAddItem = () => {
  tableData.value.push({
    orderNum: '1',
    nameWorkOrService: 'Tom',
    period: 'California',
    quantity: 'Los Angeles',
    costOfPart: 'No. 189, Grove St, Los Angeles',
    Sum: 'CA 90036',
  })
}

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
</style>