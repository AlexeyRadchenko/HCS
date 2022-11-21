<template>
    <el-dialog v-model="dialogVisible" title="Документы ЕГРН" width="80%" draggable>
        <span>Удаление записи c id:{{ egrnDocs  }}</span>
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
  expose: ['dialogVisible', 'rowIdForDel'],
  setup() {
    
  },
  data() {
    return {
        dialogVisible: false,
        egrnDocs: [],
    }
  },

}
</script>  