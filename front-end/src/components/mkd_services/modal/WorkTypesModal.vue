<template>
    <div class="mkd-services-work-types-wrapper-conteiner">
        <el-dialog v-model="dialogTypeOfWorksTableVisibleSub" title="Реестры работ" width="1250">
          <el-row>
            <el-col :span="6" style="margin-left: 1em; margin-bottom: 1em;"><el-input v-model="searchInput" style="width: 340px" placeholder="Поск по справочнику" clearable /></el-col>
          </el-row>
          <el-table :data="genTableData" :span-method="spanMethod">
            <el-table-column prop="work" label="Перечень услуг и работ по содержанию и текущему ремонту общего имущества в многоквартирном доме" width="350">
              <template #default="scope">
                <div style="display: flex; align-items: center">
                  <span style="color: blueviolet" v-if="scope.row.type == 'mainwork'">{{ scope.row.work }}</span>
                  <span style="color: green" v-else-if="scope.row.type == 'subwork'">{{ scope.row.work }}</span>
                  <span style="color: red" v-else>{{ scope.row.work }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="workInclude" label="Cостав работ" width="525" />
            <el-table-column prop="period" label="Периодичность выполнения работ" width="125" />
            <el-table-column prop="base" label="Обоснование" width="200" />
          </el-table>
        </el-dialog>
    </div>
</template>

<script setup>
// Импортируйте необходимые функции, если нужно
import { ref, reactive, computed, onMounted, watch, defineModel, toRaw } from 'vue';

const dialogTypeOfWorksTableVisibleSub = defineModel('dialogTypeOfWorksTableVisibleSub')
const props = defineProps({
  worksMainRefBook: Array,
  worksSubRefBook: Array,
  worksFixRefBook: Array,
})

const searchInput = ref('')
const genTableData = computed(() => {
    console.log("1111111111111111", props.worksMainRefBook)
    let dataArr = []
    props.worksMainRefBook.forEach(mainWelement => {
      dataArr.push({
        work: mainWelement.work,
        workInclude: '',
        period: '',
        base: '',
        type: 'mainwork',
      });
      props.worksSubRefBook.forEach(subWelement => {
        if (subWelement.mainwork_id == mainWelement.id){
          dataArr.push({
            work: subWelement.work,
            workInclude: subWelement.ext_works,
            period: subWelement.period,
            base: subWelement.base,
            type: subWelement.workType
          })
        }
      });
      dataArr.push({
        work: 'Устранение выявленных неисправностей',
        workInclude: '',
        period: '',
        base: '',
        type: 'fixwork',
      });
      props.worksFixRefBook.forEach(fixWelement => {
        if (fixWelement.mainwork_id == mainWelement.id) {
          dataArr.push({
            work: fixWelement.work,
            workInclude: fixWelement.ext_works,
            period: fixWelement.period,
            base: fixWelement.base,
            type: fixWelement.workType
          })
        }
      })
    });
    
    if (searchInput.value.trim()) {
      return dataArr.filter(item => item.work.toLowerCase().includes(searchInput.value.toLowerCase()));
    }
    return dataArr
})


const spanMethod = ({ row, column, rowIndex, columnIndex }) => {
  let rowSpan = 0
  //console.log(cloneTableData.value[0].work)
  //console.log(row.work)
  //console.log('form table datga', tableData.value[0].work)
  if (row.type === 'fix') {
    return
  }
  if (columnIndex === 0) {
    if (rowIndex >1 && genTableData.value[rowIndex-1].work === row.work) {
      rowSpan++;
    }else if (rowIndex >1 && genTableData.value[rowIndex-1].work != row.work && rowSpan > 0) {
      return { rowspan: rowSpan, colspan: 0}
    }else{
      return 
    }  

    /*} else if (rowIndex === 1) {
      return { rowspan: 0, colspan: 0 }; // Не отображать повторяющуюся ячейку
    }*/
  }
};

onMounted(() => {
  console.log('Компонент был смонтирован!');
});
</script>

<style scoped>

</style>
  