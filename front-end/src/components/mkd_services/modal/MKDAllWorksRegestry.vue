<template>
    <div class="mkd-all-works-register-wrapper-conteiner">
        <el-dialog v-model="dialogAllWorksRegisterVisibleSub" title="Реестр актов формы КС-2" width="1250">
            <el-container>
                <main>
                <el-row><el-col :span="24">Выбор отченого периода, кнопка формирования файла для печати</el-col></el-row>
                <el-row>
                    <el-col :span="24">
                        <el-tabs type="border-card">
                            <el-tab-pane label="Сантехнические работы">
                                <el-table :data="tableDataWaterWorks" style="width: 100%" max-height="450">
                                    <el-table-column fixed prop="date" label="№ П/П" width="80" />
                                    <el-table-column prop="name" label="Адреса:" width="200" />
                                    <el-table-column prop="state" label="Вид работ" width="570" />
                                    <el-table-column prop="city" label="№ сметы" width="120" />
                                    <el-table-column prop="address" label="Тек. цена" width="120" />
                                    <el-table-column fixed="right" label="Строка" min-width="90">
                                    <template #default="scope">
                                        <el-button
                                        link
                                        type="primary"
                                        size="small"
                                        @click.prevent="deleteRow(scope.$index)"
                                        >
                                        Remove
                                        </el-button>
                                    </template>
                                    </el-table-column>
                                </el-table>
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
import { ref, reactive, computed, onMounted, watch, defineModel, toRaw } from 'vue';

const dialogAllWorksRegisterVisibleSub = defineModel('dialogAllWorksRegisterVisibleSub')
const tableDataWaterWorks = ref([
  {
    date: '1',
    name: '50 лет Победы - 22',
    state: 'Текущий ремонт инженерных сетей',
    city: '15/2024',
    address: '10530',
    zip: 'CA 90036',
  },
  {
    date: '1',
    name: 'Косомонавтов 30',
    state: 'Текущий ремонт инженерных сетей',
    city: '15/2024',
    address: '10530',
    zip: 'CA 90036',
  },
  {
    date: '1',
    name: 'Космонавтов 22',
    state: 'Текущий ремонт инженерных сетей',
    city: '15/2024',
    address: '10530',
    zip: 'CA 90036',
  },
])



onMounted(() => {
  console.log('Компонент был смонтирован!');
});
</script>

<style scoped>

</style>
  