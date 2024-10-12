
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
                </el-row>
                <el-row>
                  <el-col :span="10">
                    Поля для выбора работ, периодичности, количества ел, стоимости, цена
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