<template>
    <el-dialog v-model="dialogVisible" title="Отмененные судебные документы" width="50%" draggable>
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

export default {
  expose: ['dialogVisible'],
  setup() {
    
  },
  data() {
    return {
        dialogVisible: false,

    }
  }
}

</script>