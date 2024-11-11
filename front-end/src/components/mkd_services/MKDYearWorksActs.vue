<template>
    <div class="mkd-services-year-works-act-wrapper-conteiner">
      <el-row :gutter="20">
        <el-col :span="2">
            <el-date-picker
                v-model="selectedActYear"
                type="year"
                placeholder="Год"
                style="width: 100%"
                value-format="YYYY-MM-DD"
            />
        </el-col>
        <el-col :span="5">
            <el-button type="primary" @click.prevent="generate_year_act">Сформировать</el-button>
        </el-col>
      </el-row>
      <el-row class="mkd-services-year-works-act-row">
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
import { get_year_files_list_by_house, generate_year_file_by_house_and_year } from '../../http/mkd-works-http-common'

const props = defineProps({
  selectedHouseId: String,
  selectedCompanyId: String,
  selectedHouseName: String,
})

const activeTabYear = defineModel('activeTabYear')
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

const showTab = () => {
  console.log(activeTabYear.value)
}

watch(activeTabYear, async () => {
  console.log('year act watch', activeTabYear)
  const response = await get_year_files_list_by_house(props.selectedHouseId);
  tableData.value = response.data;
});

const generate_year_act = () => {
  generate_year_file_by_house_and_year(selectedActYear.value, props.selectedHouseId).then((response) => {
    console.log(response)
  }).catch((error) => {
    console.error('Error:', error);
  });
}


onMounted(() => {
  console.log('Компонент был смонтирован!');
});
</script>

<style scoped>
.mkd-services-year-works-act-row {
  margin-top: 1em;
}
</style>
  