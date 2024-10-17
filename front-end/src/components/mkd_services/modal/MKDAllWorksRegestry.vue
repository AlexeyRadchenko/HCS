<template>
    <div class="mkd-all-works-register-wrapper-conteiner">
        <el-dialog v-model="dialogAllWorksRegisterVisibleSub" title="Реестр актов формы КС-2" width="1250">
            <el-container>
                <main>
                <el-row>
                  <el-col :span="5">
                    <el-date-picker
                      v-model="reportMonth"
                      type="month"
                      placeholder="Выберите месяц"
                    />
                  </el-col>
                  <el-col :span="6">
                    <el-button type="info" style="width: 100%">Сформировать за выбранный месяц</el-button>
                  </el-col>
                </el-row>
                <el-row class="mkd-all-works-register-rows-top-m">
                  <el-col :span="5">
                    <el-date-picker
                      v-model="reportYear"
                      type="year"
                      placeholder="Выберите год"
                    />
                  </el-col>
                  <el-col :span="6">
                    <el-button type="info" style="width: 100%">Сформировать за выбранный год</el-button>
                  </el-col>
                </el-row>
                <el-row class="mkd-all-works-register-rows-top-m">
                    <el-col :span="24">
                        <el-tabs type="border-card">
                            <el-tab-pane label="Сантехнические работы">
                                <el-table :data="tableDataWaterWorks" style="width: 100%" max-height="450">
                                    <el-table-column fixed prop="order" label="№ П/П" width="80" />
                                    <el-table-column prop="address" label="Адреса:" width="200" />
                                    <el-table-column prop="work" label="Вид работ" width="570" />
                                    <el-table-column prop="smetaNum" label="№ сметы" width="120" />
                                    <el-table-column prop="price" label="Тек. цена" width="120" />
                                    <el-table-column fixed="right" label="Строка" min-width="90">
                                    <template #default="scope">
                                        <el-button
                                        link
                                        type="primary"
                                        size="small"
                                        @click.prevent="deleteRowWaterWorks(scope.$index)"
                                        >
                                        Remove
                                        </el-button>
                                    </template>
                                    </el-table-column>
                                </el-table>
                                <el-row class="mkd-all-works-register-rows-top-m">
                                  <el-col :span="4"><el-text type="success" size="large" tag="b">Итого</el-text></el-col>
                                  <el-col :span="4" :offset="16"><el-text type="success" size="large" tag="b">{{ sumTableDataWaterWorks }}</el-text></el-col>
                                </el-row>
                            </el-tab-pane>
                            <el-tab-pane label="Электромонтажные работы">Config</el-tab-pane>
                            <el-tab-pane label="Общестроительнрые работы">Role</el-tab-pane>
                            <el-tab-pane label="Использование гидроподъёмника">Task</el-tab-pane>
                            <el-tab-pane label="Дератизация и дезинсекция подвалов">Task</el-tab-pane>
                        </el-tabs>
                    </el-col>
                </el-row>
                </main>
            </el-container>
        </el-dialog>
    </div>
</template>

<script setup>
// Импортируйте необходимые функции, если нужно
import { ref, reactive, computed, onMounted, watch, defineModel, toRaw, effectScope } from 'vue';
import Decimal from 'decimal.js';
//https://github.com/MikeMcl/decimal.js
Decimal.set({ rounding: 2 })

const dialogAllWorksRegisterVisibleSub = defineModel('dialogAllWorksRegisterVisibleSub')
const reportMonth = ref('')
const reportYear = ref('')
const tableDataWaterWorks = ref([
  {
    order: '1',
    address: '50 лет Победы - 22',
    work: 'Текущий ремонт инженерных сетей',
    smetaNum: '15/2024',
    price: '10530',
    zip: 'CA 90036',
  },
  {
    order: '1',
    address: 'Косомонавтов 30',
    work: 'Текущий ремонт инженерных сетей',
    smetaNum: '15/2024',
    price: '10530',
    zip: 'CA 90036',
  },
  {
    order: '1',
    address: 'Космонавтов 22',
    work: 'Текущий ремонт инженерных сетей',
    smetaNum: '15/2024',
    price: '10530',
    zip: 'CA 90036',
  },
])

const sumTableDataWaterWorks = computed(() => {
  let sum = new Decimal(0)
  let price = new Decimal(NaN)
  tableDataWaterWorks.value.forEach(element => {
    price = new Decimal(element.price)
    console.log(price)
    console.log('element', element.price)
    sum = Decimal.add(sum, price)
    console.log('sum', sum)
  });
  return sum.toFixed(2).toString()
})

const deleteRowWaterWorks = (index) => {
  tableDataWaterWorks.value.splice(index, 1)
}

onMounted(() => {
  console.log('Компонент был смонтирован!');
});
</script>

<style scoped>
  .mkd-all-works-register-rows-top-m {
    margin-top: 1em;
  }
</style>
  