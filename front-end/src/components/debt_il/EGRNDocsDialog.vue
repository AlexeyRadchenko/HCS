<template>
    <el-dialog v-model="dialogVisible" title="Документы ЕГРН" width="80%" draggable>
        <el-row>
          <el-col :span="24">
            <el-table :data="egrnData" style="width: 100%">
              <el-table-column prop="date" label="Дата" width="180" />
              <el-table-column prop="number" label="Номер" width="180" />
              <el-table-column label="Документ">
                <template #default="scope">
                  <button @click="egrnDocDownload(scope.row.file)">
                    <font-awesome-icon :icon="['fas', 'fa-file-pdf']"  v-if="'pdf' === fileExtension(scope.row.file) " size="4x" />
                    <font-awesome-icon :icon="['fas', 'fa-file-word']"  v-if="'docx' === fileExtension(scope.row.file) " size="4x" />
                    <font-awesome-icon :icon="['fas', 'fa-file-excel']"  v-if="'xlsx' === fileExtension(scope.row.file) " size="4x" />
                    <font-awesome-icon :icon="['fas', 'fa-file-file']"  v-if="!(['pdf', 'docx', 'xlsx'].includes(fileExtension(scope.row.file)))" size="4x" />
                  </button>
                </template>  
              </el-table-column>
              <el-table-column prop="note" label="Примечание" width="350" />
              <el-table-column label="Редактировать сведения" width="190" align="center">
                <template #default="scope">
                  <el-button
                  @click.prevent="deleteRow(scope.$index)"
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
              <el-form-item label="Дата">
                <el-date-picker
                  v-model="formEGRNInline.egrnDocDate"
                  type="date"
                  placeholder="Выберите дату"
                />
              </el-form-item>
              <el-form-item label="Номер">
                <el-input v-model="formEGRNInline.egrnDocNumber" placeholder="Please input" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="onSubmit">Query</el-button>
              </el-form-item>
            </el-form> 
          </el-col>
        </el-row>
        <span>Сведения из ЕГРН для испольнительного листа {{ il_number  }}</span>
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
export default {
  expose: ['dialogVisible', 'rowId', 'il_number'],
  setup() {
    
  },
  data() {
    return {
        dialogVisible: false,
        egrnDocs: [],
        rowId: null,
        il_number: '',
        egrnData: [
          {
            date: '2016-05-03',
            number: 'б-3412',
            file: '/fdfsdf/sdfsdf/sdfs.xlsx',
            note: 'Дополнение к файлу',
          },
          {
            date: '2016-05-12',
            number: 'T-2342',
            file: '/fdfsdf/sdfsdf/sdfs.pdf',
            note: 'Дополнение к файлу',
          },
        ],
        formEGRNInline: {
          egrnDocDate: '',
          egrnDocNumber: '',
        }
    }

  },
   methods: {
    egrnDocDownload (url_file) {
      console.log(url_file)
    },
    fileExtension (filePath) {
      return filePath.split('.').pop()
    },
    onSubmit () {
      console.log('pushhhhhh!')
    }
  },
  computed: {
    
  }
}
</script>  