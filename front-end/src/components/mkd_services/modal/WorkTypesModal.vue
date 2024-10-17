<template>
    <div class="mkd-services-work-types-wrapper-conteiner">
        <el-dialog v-model="dialogTypeOfWorksTableVisibleSub" title="Реестры работ" width="1250">
          <el-table :data="tableData " :span-method="spanMethod">
            <el-table-column prop="work" label="Перечень услуг и работ по содержанию и текущему ремонту общего имущества в многоквартирном доме" width="350">
              <template #default="scope">
                <div style="display: flex; align-items: center">
                  <span style="color: blueviolet" v-if="scope.row.type != 'fix'">{{ scope.row.work }}</span>
                  <span style="color: red" v-else="scope.row.type">{{ scope.row.work }}</span>
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

const mainWorks = [
  {
    id: '1', 
    work: 'Работы, выполняемые в отношении всех видов фундаментов',
    type: 'main'
  },
  {
    id: '2',
    work: 'Работы, выполняемые в зданиях с подвалами (ряд работ также учтен в разделах: 1., 3., 17., 22)',
    type: 'main'
  },
]

const subWorks = [{
  id: '1',
  work: 'Проверка соответствия параметров вертикальной планировки территории вокруг здания \
  проектным параметрам. Проверка технического состояния видимых частей конструкций\
  с выявлением: признаков неравномерных осадок фундаментов всех типов;коррозии арматуры, расслаивания, трещин, выпучивания, отклонения от вертикали в\
  домах с бетонными, железобетонными и каменными фундаментами; поражения гнилью\
  и частичного разрушения деревянного основания в домах со столбчатыми или свайными деревянными фундаментами;\
  при выявлении нарушений - разработка контрольных шурфов в местах обнаружения дефектов, детальное обследование и составление плана мероприятий по устранению\
  причин нарушения и восстановлению эксплуатационных свойств конструкций; проверка состояния гидроизоляции фундаментов и систем водоотвода фундамента. Определение\
  и документальное фиксирование температуры вечномерзлых грунтов для фундаментов в условиях вечномерзлых грунтов.',
  mainWorkId: '1',
  period: '2 раза в год',
  base: 'П. 13(1) Правил содержания общего имущества в многоквартирном доме, утвержденных постановлением Правительства РФ от 13.08.2006 г. №491',
  type: 'sub',
},
{
  id: '2',
  work: 'Проверка температурно-влажностного режима подвальных помещений и при выявлении нарушений устранение причин его нарушения; проверка состояния помещений\
  подвалов, входов в подвалы и приямков, принятие мер, исключающих подтопление, захламление, загрязнение и загромождение таких помещений, а также мер, обеспечивающих\
  их вентиляцию в соответствии с проектными требованиями; контроль за состоянием дверей подвалов и технических подполий, запорных устройств на них.',
  mainWorkId: '2',
  period: '2 раза в год',
  base: 'П. 13(1) Правил содержания общего имущества в многоквартирном доме, утвержденных постановлением Правительства РФ от 13.08.2006 г. №491',
  type: 'sub',
},
]
const fixWorks = [{
  id: '1',
  work: 'Устранение повреждений фундаментов',
  workInclude: 'Устранение повреждений каменных фундаментов: разборка негодной части фундамента. Заготовка и установка при необходимости двутавровых балок.\
Пробивка отверстий и заделка их кирпичами. Кладка фундаментов из кирпичей с перевязкой со старой кладкой. Устройство горизонтальной изоляции\
рулонными материалами в два слоя. Сверление отверстий в фундаменте с установкой трубок. Заделка зазоров между трубками и поверхностью кладки цементным раствором. Нагнетание раствора\
через трубки в кладку фундамента с загрузкой смеси в растворонагнетатель. Устранение повреждений бутовых фундаментов: разборка негодной части фундамента. Заготовка и\
установка при необходимости двутавровых балок. Пробивка отверстий и заделка их камнями. Кладка фундаментов из камней с перевязкой со старой кладкой. Устройство горизонтальной изоляции рулонными\
материалами в два слоя. Сверление отверстий в фундаменте с установкой трубок. Заделка зазоров между трубками и поверхностью кладки цементным раствором. Нагнетание раствора через\
трубки в кладку фундамента с загрузкой смеси в растворонагнетатель. Устранение повреждений железобетонных фундаментов: разборка негодной части фундамента. Заготовка и установка при необходимости двутавровых\
балок. Подъем и установка блоков с заливкой швов и заделкой стыков. Устройство горизонтальной изоляции рулонными материалами в два слоя.',
  mainWorkId: '1',
  period: 'По мере необходимости',
  base: 'Дефектные ведомости',
  type: 'fix',
},
{
  id: '2',
  work: 'Осушение',
  workInclude: 'Вычерпывание воды ведрами с выноской (33%11). Установка и передвижка насоса с прокладкой шлангов и устройством водостоков. Откачка воды ручными (33%) или электрическими (34%) насосами.',
  mainWorkId: '1',
  period: 'По мере необходимости',
  base: 'Акт осмотра (обследования)',
  type: 'fix',
},
{
  id: '3',
  work: 'Восстановление ограждающих решеток',
  workInclude: 'Снятие решеток. Выправка решеток с очисткой от коррозии. Расчистка гнезд. Установка решеток на место с заливкой гнезд.',
  mainWorkId: '2',
  period: 'По мере необходимости',
  base: 'Дефектные ведомости',
  type: 'fix',
},
{
  id: '4',
  work: 'Восстановление (ремонт) освещения подвалов с открытой проводкойОсушение',
  workInclude: 'Снятие проводок с отсоединением жил. Демонтаж конструкций, изоляторов. Заготовка провода или кабеля. Прокладка. Соединение жил. Прозвонка. \
Снятие перегоревшей лампы. Установка новой лампы. Проверка работы. Снятие выключателей с отсоединением их от проводов. Установка новых выключателей с подсоединением проводов. Проверка\
работы выключателей. Отсоединение жил проводов от зажимов в патроне. Присоединение проводов к зажимам нового патрона. Опробование работы патрона.',
  mainWorkId: '2',
  period: 'По мере необходимости',
  base: 'Дефектные ведомости',
  type: 'fix',
}   
]

const genTableData = (mainWorks, subWorks, fixWorks) => {
    let dataArr = []
    mainWorks.forEach(mainWelement => {
      subWorks.forEach(subWelement => {
        if (subWelement.mainWorkId == mainWelement.id){
          dataArr.push({
            work: mainWelement.work,
            workInclude: subWelement.work,
            period: subWelement.period,
            base: subWelement.base,
            type: subWelement.type
          })
        }
      });
      dataArr.push({
        work: 'Устранение выявленных неисправностей',
        workInclude: '',
        period: '',
        base: '',
        type: 'fix',
      });
      fixWorks.forEach(fixWelement => {
        if (fixWelement.mainWorkId == mainWelement.id) {
          dataArr.push({
            work: fixWelement.work,
            workInclude: fixWelement.workInclude,
            period: fixWelement.period,
            base: fixWelement.base,
            type: fixWelement.type
          })
        }
      })
    });
    return dataArr
}


/*const tableData = ref([
{ work: 'John', workInclude: '2024-10-01', period: 'New York', base: 'asdasd', fixWorkId: '1' },
{ work: 'John', workInclude: '2024-10-01', period: 'New York', base: 'asdasd', fixWorkId: '1' },
{ work: 'Doe', workInclude: '2024-10-02', period: 'Los Angeles', base: 'asdasd', fixWorkId: '1' },
{ work: 'Doe', workInclude: '2024-10-03', period: 'Los Angeles', base: 'asdasd', fixWorkId: '1' },
]);*/

const tableData = ref(genTableData(mainWorks, subWorks, fixWorks))
const cloneTableData = toRaw(tableData)
const spanMethod = ({ row, column, rowIndex, columnIndex }) => {
  let rowSpan = 0
  //console.log(cloneTableData.value[0].work)
  //console.log(row.work)
  //console.log('form table datga', tableData.value[0].work)
  if (row.type === 'fix') {
    return
  }
  if (columnIndex === 0) {
    if (rowIndex >1 && cloneTableData.value[rowIndex-1].work === row.work) {
      rowSpan++;
    }else if (rowIndex >1 && cloneTableData.value[rowIndex-1].work != row.work && rowSpan > 0) {
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
  