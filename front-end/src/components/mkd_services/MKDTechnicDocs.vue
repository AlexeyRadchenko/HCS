<template>
    <div class="mkd-technic-docs-wrapper-conteiner">
      <el-text class="mx-1" size="large">{{ selectedCompanyId }} - {{ selectedHouseId }}</el-text>
      <el-row>
        <el-col :span="24">
            <el-table :data="tableData" style="width: 100%" max-height="900">
                <el-table-column fixed prop="numOrder" label="№ П/П" width="90" />
                <el-table-column prop="actYear" label="Год" width="100" />
                <el-table-column prop="actDate" label="Дата акта" width="100" />
                <el-table-column prop="actNum" label="№ Акта" width="140" />
                <el-table-column prop="actFile" label="Файл" width="120" />
                <el-table-column fixed="right" label="Operations" min-width="120">
                <template #default="scope">
                    <el-button
                    link
                    type="primary"
                    @click.prevent="showActData(scope.row.actNum)"
                    >
                    Подробнее
                    </el-button>
                </template>
                </el-table-column>
            </el-table>
        </el-col>
      </el-row>
    </div>
</template>

<script setup>
// Импортируйте необходимые функции, если нужно
import { ref, reactive, computed, onMounted, watch, defineModel, toRaw } from 'vue';

const props = defineProps({
  selectedHouseId: String,
  selectedCompanyId: String,
  selectedHouseName: String,
})

const selectedActYear = ref('')
const tableData = ref([
  {
    numOrder: 1,
    actYear: '2024',
    actDate: '01.01.2024',
    actNum: 'Los Angeles',
    actFile: 'url',
  },
  {
    numOrder: 2,
    actYear: '2024',
    actDate: '01.01.2024',
    actNum: 'Los Angeles',
    actFile: 'url',
  },
  {
    numOrder: 3,
    actYear: '2024',
    actDate: '01.01.2024',
    actNum: 'Los Angeles',
    actFile: 'url',
  },
])

const showActData = (numAct) =>{
    console.log(numAct)
}
onMounted(() => {
  console.log('Компонент был смонтирован!');
  //console.log('selectedCompanyId:', selectedCompanyId);
  //console.log('selectedHouseId:', selectedHouseId);
});
</script>

<style scoped>
.mkd-services-year-works-act-row {
  margin-top: 1em;
}
</style>
  