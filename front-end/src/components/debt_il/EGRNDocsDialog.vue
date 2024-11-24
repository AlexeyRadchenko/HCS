<template>
    <el-dialog v-model="dialogVisible" :title="'Документы ЕГРН И/Л № ' + il_number"   width="80%" draggable>
        <el-row>
          <el-col :span="24">
            <el-table :data="egrnData" style="width: 100%">
              <el-table-column prop="date" label="Дата" width="180" />
              <el-table-column prop="number" label="Номер" width="180" />
              <el-table-column prop="name" label="Наименование" width="180" />
              <el-table-column label="Документ">
                <template #default="scope">
                  <button @click="egrnDocDownload(scope.row.file, scope.row.name)" class="d-button-hover">
                    <font-awesome-icon :icon="['fas', 'fa-file-pdf']"  v-if="'pdf' === fileExtension(scope.row.file) " size="4x" />
                    <font-awesome-icon :icon="['fas', 'fa-file-word']"  v-if="'docx' === fileExtension(scope.row.file) " size="4x" />
                    <font-awesome-icon :icon="['fas', 'fa-file-excel']"  v-if="'xlsx' === fileExtension(scope.row.file) " size="4x" />
                    <font-awesome-icon :icon="['fas', 'fa-file']"  v-if="!(['pdf', 'docx', 'xlsx'].includes(fileExtension(scope.row.file)))" size="4x" />
                  </button>
                </template>  
              </el-table-column>
              <el-table-column prop="note" label="Примечание" width="350" />
              <el-table-column label="Редактировать сведения" width="190" align="center">
                <template #default="scope">
                  <el-button
                  @click.prevent="deleteRow(scope.$index, scope.row.id)"
                  type="danger"
                  >Удалить</el-button>
                </template>
              </el-table-column>  
            </el-table>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-divider />
            <span>Загрузить документ</span>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form :inline="true" :model="formEGRNInline">
              <el-form-item label="Дата" style="margin-top:-0.78em;">
                <el-date-picker
                  v-model="formEGRNInline.egrnDocDate"
                  type="date"
                  format="DD.MM.YYYY"
                  value-format="YYYY-MM-DD"
                  placeholder="Выберите дату"
                />
              </el-form-item>
              <el-form-item label="Номер">
                <el-input v-model="formEGRNInline.egrnDocNumber" />
              </el-form-item>
              <el-form-item label="Примечание к док-ту">
                <el-input v-model="formEGRNInline.egrnDocNote" />
              </el-form-item>
              <el-form-item>
                <el-upload
                  ref="uploadRef"
                  :action="upload_action_url"
                  :auto-upload="false"
                  :limit="1"
                  :headers="uploadHeaders"
                  :data="formEGRNInline"
                  :on-success="successEGRNDocUpload"
                  :on-exceed="replaceFileToPrepare"
                >
                  <template #trigger>
                    <el-button type="primary">Выбрать файл</el-button>
                  </template>

                  <el-button style="margin-left:1em;" type="success" @click="submitUpload">
                    Загрузить на сервер
                  </el-button>

                  <template #tip>
                    <div class="el-upload__tip">
                      pdf/word/excel и другие файлы размером не более 80MB.
                    </div>
                  </template>
                </el-upload>
              </el-form-item>
            </el-form> 
          </el-col>
        </el-row>
        <template #footer>
        <span class="dialog-footer">
            <el-button @click="dialogVisible = false">Отмена</el-button>
            <el-button type="primary" @click="dialogVisible = false">
            OK
            </el-button>
        </span>
        </template>
    </el-dialog>    
</template>

<script>
import { ref } from 'vue'
import secureStorage from '../../storage/secStorage'
import { debt_il_get_egrn_docs_by_id_il, debt_il_del_egrn_docs_by_egrn_doc_id, debt_il_download_egrn_docs_by_file_path } from '../../http/http-common';

export default {
  expose: ['dialogVisible', 'rowId', 'il_number'],
  setup() {
    let uploadHeaders = {
        'Authorization': 'Bearer ' + secureStorage.getItem('token')
    }
    const uploadRef = ref()
    const upload_action_url = import.meta.env.VITE_API_DEBT_IL_EGRN_UPLOAD_URL
    
    return {
      upload_action_url, uploadRef, uploadHeaders
    }
  },
  data() {
    return {
        dialogVisible: false,
        egrnDocs: [],
        rowId: null,
        il_number: '',
        egrnData: [],
        formEGRNInline: {
          egrnDocDate: '',
          egrnDocNumber: '',
          egrnDocNote: '',
          il_number: '',
          il_base_id: '',
        },
        fileList: [

        ],
    }

  },
   methods: {
    fileExtension (filePath) {
      //console.log('fp pp', this.egrnData)
      //console.log('fp', filePath)
      return filePath.split('.').pop()
    },
    submitUpload () {
      //console.log('pushhhhhh!')
      //console.log(this.fileList)
      //console.log(this.uploadRef)
      this.formEGRNInline.il_number = this.il_number
      this.formEGRNInline.il_base_id = this.rowId
      this.uploadRef.submit()
    },
    async get_egrn_docs_data_if_dialog_open (il_id) {
      this.egrnData = await debt_il_get_egrn_docs_by_id_il(il_id)
      console.log('egrnData After SHow', this.egrnData)
    },
    successEGRNDocUpload (response, file, files) {
      let response_obj = JSON.parse(response)
      this.egrnData.push(response_obj)
      console.log('egrnData after upload', this.egrnData)
      //console.log('response after upload doc', response)
    },
    replaceFileToPrepare (files, uploadFiles) {
      this.uploadRef.clearFiles()
      this.uploadRef.handleStart(files[0])
      console.log(uploadFiles)
    },
    async deleteRow (indexDataTable, id_db) {
      let res = await debt_il_del_egrn_docs_by_egrn_doc_id(id_db)
      if (res.result === 'success')
        this.egrnData.splice(indexDataTable, 1)
    },
    async egrnDocDownload (file_path, file_name) {
      await debt_il_download_egrn_docs_by_file_path (file_path, file_name)
    }, 
  },
  watch: {
    dialogVisible (visible, hide) {
      if (visible) {
        this.get_egrn_docs_data_if_dialog_open(this.rowId)   
      }
    }
  },
  
}
</script>

<style scoped>
.d-button-hover {
  cursor: pointer;
}
</style>