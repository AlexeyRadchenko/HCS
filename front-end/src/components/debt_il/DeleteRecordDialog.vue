<template>
    <el-dialog v-model="dialogVisible" title="Tips" width="30%" draggable>
        <span>Удаление записи</span>
        <template #footer>
        <span class="dialog-footer">
            <el-button @click="dialogVisible = false">Отмена</el-button>
            <el-button type="primary" @click="dialogVisible = false">
            Удалить
            </el-button>
        </span>
        </template>
    </el-dialog>    
</template>

<script>
export default {
  expose: ['dialogVisible'],
  setup() {
    
  },
  data() {
    return {
        dialogVisible: false
    }
  },

}
</script>  