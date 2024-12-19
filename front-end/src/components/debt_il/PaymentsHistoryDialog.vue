<template>
    <el-dialog v-model="dialogVisible" :title='"История платежей по и/л " + il_doc_number' width="50%" draggable>
      <el-row>
        <el-col>
          <el-table :data="paymentsHistoryData" style="width: 100%" height="250">
            <el-table-column fixed prop="date" label="Дата" width="150" />
            <el-table-column prop="type" label="Типа платежа" width="120" />
            <el-table-column prop="sum" label="Сумма" width="120" />
            <el-table-column prop="account_il.name" label="Плательщик" width="320" />
            <el-table-column prop="notes" label="Примечание" width="600" />
          </el-table>
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
import { debt_il_get_payments_il_by_id_il } from '../../http/http-common'

export default {
  expose: ['dialogVisible', 'il_base_id', 'il_doc_number'],
  setup() {
    
  },
  data() {
    return {
        dialogVisible: false,
        il_base_id: '',
        il_doc_number: '',
        paymentsHistoryData: [],

    }
  },
  methods: {
    async get_payments_data_if_dialog_open (il_id) {
      console.log(il_id)
      this.paymentsHistoryData = await debt_il_get_payments_il_by_id_il (il_id)
      //console.log('egrnData After SHow', this.egrnData)
    },
  },
  watch: {
    dialogVisible (visible, hide) {
      if (visible) {
        this.get_payments_data_if_dialog_open(this.il_base_id)
      }
    }
  },  
}

</script>