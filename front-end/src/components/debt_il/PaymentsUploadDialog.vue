<template>
    <el-dialog v-model="dialogVisible" title="Загрузка данных об оплате" width="40%" draggable>
        <el-row>
            <el-col :span="12">
                <el-upload
                    ref="upload"
                    class="upload-demo"
                    action="http://localhost:8090/api/v1/debt_il_service/il/upload/payments_il"
                    :limit="1"
                    :multiple='false'
                    :headers="uploadHeaders"
                    :on-success="successUploadPaymentFile"
                >
                    <el-button type="primary">Click to upload</el-button>
                    <template #tip>
                    <div class="el-upload__tip">
                        xlsx files with a size less than 500KB.
                    </div>
                    </template>
                </el-upload>
            </el-col>
            <el-col :span="12">
                <el-button type="primary">Сформировать данные</el-button>
            </el-col>
        </el-row>
        
        <template #footer>
        <span class="dialog-footer">
            <el-button @click="dialogVisible = false">Отмена</el-button>
            <el-button type="primary" @click="dialogVisible = false">
            Сохранить
            </el-button>
        </span>
        </template>
    </el-dialog>    
</template>

<script>
import secureStorage from '../../storage/secStorage'


export default {
  expose: ['dialogVisible', 'rowIdForDel'],
  setup() {
    let uploadHeaders = {
        'Authorization': 'Bearer ' + secureStorage.getItem('token')
    }
    return {
        uploadHeaders
    }
  },
  data() {
    return {
        dialogVisible: false,
        rowIdForDel: null,
        upload: null,

    }
  },
  methods: {
    successUploadPaymentFile (response) {
        console.log(response)
    }
  }
}
</script>