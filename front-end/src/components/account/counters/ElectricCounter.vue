<template>
    <div>
        <el-row>
            <el-col :span="24">
                <el-divider content-position="left"><h2>Электросчётчики</h2></el-divider>
            </el-col>
        </el-row>
        <el-row :gutter="12" v-for="(row, index) in electricRows" :key="index" class="counter-row">
            <el-col :span="6" v-for="(item, innerindex) in row" :key="item.id" >
            <el-card shadow="always" class="electric-counter-bg">
                <template #header>
                    <div class="card-header">
                        <font-awesome-icon :icon="['fas', 'bolt']" size="1x" />
                        <span class="electric-card-header-text"><h3>{{ 'Электросчетчик № ' + item.serial_number }}</h3></span>
                    </div>
                </template>
                <el-row>
                    <el-col :span="14"><h4>Дата последней поверки:</h4></el-col><el-col :span="10" class="card-data">{{ dateCounterView(item.setup_date) }}</el-col>
                </el-row>
                <el-row>
                    <el-col :span="14"><h4>Дата предыдущих показаний:</h4></el-col><el-col :span="10" class="card-data">{{ dateCounterView(item.last_date_update) }}</el-col>
                </el-row>
                <el-row v-if="item.type === 'single'">
                    <el-col :span="14"><h4>Прошлые показания:</h4></el-col><el-col :span="10" class="card-data">{{ item.old_simple_data }} кВт/ч</el-col>
                </el-row>
                <el-row v-if="item.type === 'double'">
                    <el-col :span="14"><h4>Прошлые показания день:</h4></el-col><el-col :span="10" class="card-data">{{ item.old_day_data }} кВт/ч</el-col>
                </el-row>
                <el-row  v-if="item.type === 'double'">
                    <el-col :span="14"><h4>Прошлые показания ночь:</h4></el-col><el-col :span="10" class="card-data">{{ item.old_night_data }} кВт/ч</el-col>
                </el-row>
                <el-divider border-style="dashed" class="electric-divider-color" />
                <el-row>
                    <el-col :span="14"><h4>Дата текущих показаний:</h4></el-col><el-col :span="10" class="card-data">{{ dateCounterView(item.date_update) }}</el-col>
                </el-row>
                <el-row v-if="item.type === 'single'">
                    <el-col :span="14"><h4>Текущие показания:</h4></el-col><el-col :span="10" class="card-data">{{ item.simple_data }} кВт/ч</el-col>
                </el-row>
                <el-row v-if="item.type === 'double'">
                    <el-col :span="14"><h4>Текущие показания день:</h4></el-col><el-col :span="10" class="card-data">{{ item.day_data }} кВт/ч</el-col>
                </el-row>
                <el-row v-if="item.type === 'double'">
                    <el-col :span="14"><h4>Текущие показания ночь:</h4></el-col><el-col :span="10" class="card-data">{{ item.night_data }} кВт/ч</el-col>
                </el-row>
                <el-row v-if="item.type === 'single'">
                    <el-col :span="14"><h4>Текущий расход:</h4></el-col><el-col :span="10" class="card-data">{{ item.simple_diff }} кВт/ч</el-col>
                </el-row>
                <el-row v-if="item.type === 'double'">
                    <el-col :span="14"><h4>Текущий расход день:</h4></el-col><el-col :span="10" class="card-data">{{ item.day_diff }} кВт/ч</el-col>
                </el-row>
                <el-row v-if="item.type === 'double'">
                    <el-col :span="14"><h4>Текущий расход ночь:</h4></el-col><el-col :span="10" class="card-data">{{ item.night_diff }} кВт/ч</el-col>
                </el-row>
                <el-divider border-style="dashed" class="electric-divider-color" />
                <el-row v-if="item.type === 'single'">
                    <el-col :span="14">
                        <el-input
                        v-model="electricInputs[innerindex].simple_val"
                        placeholder="0"
                        size="large"
                        v-mask="electricInputMasks"
                        @keyup.enter="sendDataElectricCounter(
                            electricInputs[innerindex], item.date_update, innerindex, item.old_simple_data, item.old_day_data, item.old_night_data, item.type)"
                        />
                    </el-col>
                    <el-col :span="2">
                        <el-popover
                            placement="top-start"
                            title="Подсказка"
                            :width="400"
                            trigger="hover"
                            content="Число после запятой/точки на счетчике вводить не нужно, т.е. если на счетчике 4323.7 пишите 4323"
                        >
                            <template #reference>
                                <div style="float:left; margin-left: 0.6rem; margin-top: 0.22rem;">
                                    <font-awesome-icon :icon="['fas', 'question-circle']" size="2x" />
                                </div>
                            </template>
                        </el-popover>
                    </el-col>
                    <el-col :span="8" class="card-data">
                        <el-button
                        size="large"
                        @click="sendDataElectricCounter(
                            electricInputs[innerindex], item.date_update, innerindex, item.old_simple_data, item.old_day_data, item.old_night_data, item.type)"
                        :loading="electricInputs[innerindex].loading">Записать</el-button>
                    </el-col>
                </el-row>
                <el-row v-if="item.type === 'double'">
                    <el-col :span="14">
                        <el-input
                        v-model="electricInputs[innerindex].day_val"
                        placeholder="0"
                        size="large"
                        v-mask="electricInputMasks"
                        @keyup.enter="sendDataElectricCounter(
                            electricInputs[innerindex], item.date_update, innerindex, item.old_simple_data, item.old_day_data, item.old_night_data, item.type)"
                        />
                    </el-col>
                    <el-col :span="2">
                        <el-popover
                            placement="top-start"
                            title="Подсказка"
                            :width="400"
                            trigger="hover"
                            content="Число после запятой/точки на счетчике вводить не нужно, т.е. если на счетчике 4323.7 пишите 4323"
                        >
                            <template #reference>
                                <div style="float:left; margin-left: 0.6rem; margin-top: 0.22rem;">
                                    <font-awesome-icon :icon="['fas', 'question-circle']" size="2x" />
                                </div>
                            </template>
                        </el-popover>
                    </el-col>
                </el-row>
                <el-row v-if="item.type === 'double'">
                    <el-col :span="14">
                        <el-input
                        v-model="electricInputs[innerindex].night_val"
                        placeholder="0"
                        size="large"
                        v-mask="electricInputMasks"
                        @keyup.enter="sendDataElectricCounter(
                            electricInputs[innerindex], item.date_update, innerindex,  item.old_simple_data,  item.old_day_data, item.old_night_data, item.type)"
                        />
                    </el-col>
                    <el-col :span="2">
                        <el-popover
                            placement="top-start"
                            title="Подсказка"
                            :width="400"
                            trigger="hover"
                            content="Число после запятой/точки на счетчике вводить не нужно, т.е. если на счетчике 4323.7 пишите 4323"
                        >
                            <template #reference>
                                <div style="float:left; margin-left: 0.6rem; margin-top: 0.22rem;">
                                    <font-awesome-icon :icon="['fas', 'question-circle']" size="2x" />
                                </div>
                            </template>
                        </el-popover>
                    </el-col>
                </el-row>
                <el-row v-if="item.type === 'double'">
                    <el-col :span="12" :offset="6" class="card-data">
                        <el-button
                        style="width:100%"
                        size="large"
                        @click="sendDataElectricCounter(
                            electricInputs[innerindex], item.date_update, innerindex, item.old_simple_data, item.old_day_data, item.old_night_data, item.type)"
                        :loading="electricInputs[innerindex].loading">Записать</el-button>
                    </el-col>
                </el-row>
                <el-row style="height: 1.9rem;">
                    <el-col :span="24">
                        <el-alert
                         :title="electricInputs[innerindex].message"
                         type="success"
                         show-icon
                         v-if="electricInputs[innerindex].success"
                         @close="alertsClose(electricInputs[innerindex])" /> 
                        <el-alert
                        v-show="electricInputs[innerindex].error"
                        :title="electricInputs[innerindex].message" 
                        type="error"
                        show-icon v-if="electricInputs[innerindex].error"
                        @close="alertsClose(electricInputs[innerindex])" />
                    </el-col>
                </el-row>
            </el-card>
            </el-col>
        </el-row>
    </div> 
</template>

<script>
import { defineComponent } from 'vue'
import moment from 'moment/dist/moment'
import ru from 'moment/dist/locale/ru'
import { put_electric_counter_data_by_counter_id } from '../../../http/account-http-common'

export default defineComponent({
    setup() {
        moment.updateLocale('ru', ru)
        return { moment }
    },
    data () {
        return {
            electricInputs: [],
            electricInputMasks: ['#####'],
        }
    },
    props: {
        electricCounters: Array,
        account: String,
    },
    methods: {
        dateCounterView (date) {
            if (date === 'now') {
                return moment().format('L')
            }
            return moment(date).format('L')
        },
        resposneViewer(response, counterData) {
            if (response.status === 'OK') {
                if (counterData.error) {
                    counterData.error = false
                }
                counterData.success = true
                counterData.message = response.message
            }

            if (response.status === 'error') {
                if (counterData.success) {
                    counterData.success = false
                }
                counterData.error = true
                counterData.message = response.message
            }
        },
        updateViewCounter (index, response, dataNow, oldDate, simple_oldCounterData, day_oldCounterData, night_oldCounterData) {
            if (response.exch) {
                this.electricCounters[index].simple_data = dataNow.simple_val
                this.electricCounters[index].day_data = dataNow.day_val
                this.electricCounters[index].night_data = dataNow.night_val
                this.electricCounters[index].date_update = 'now'
                this.electricCounters[index].old_simple_data = simple_oldCounterData
                this.electricCounters[index].old_day_data = day_oldCounterData
                this.electricCounters[index].old_night_data = night_oldCounterData
                this.electricCounters[index].last_date_update = oldDate
                this.electricCounters[index].simple_diff = response.simple_difference
                this.electricCounters[index].day_diff = response.day_difference
                this.electricCounters[index].night_diff = response.night_difference
            }else{
                this.electricCounters[index].simple_data = dataNow.simple_val
                this.electricCounters[index].day_data = dataNow.day_val
                this.electricCounters[index].night_data = dataNow.night_val
                this.electricCounters[index].date_update = 'now'
                this.electricCounters[index].simple_diff = response.simple_difference
                this.electricCounters[index].day_diff = response.day_difference
                this.electricCounters[index].night_diff = response.night_difference
            }
        },
        alertsClose (alertState) {
            console.log(alertState)
            if (alertState.success) {
                alertState.success = false
            }
            if (alertState.error) {
                alertState.error = false
            } 
        },
        async sendDataElectricCounter (counterData, oldCounterDate, index, simple_oldCounterData, day_oldCounterData, night_oldCounterData, type) {
            counterData.loading = true
            var counterDataForm = new FormData()
            if (counterData.simple_val) {
                counterDataForm.append('counter_id', counterData.id)
                counterDataForm.append('counter_simple_data', counterData.simple_val)
                counterDataForm.append('old_counter_simple_data', simple_oldCounterData)
                counterDataForm.append('old_date_update', oldCounterDate)
                counterDataForm.append('type', type)
            } else if (counterData.day_val && counterData.night_val) {
                counterDataForm.append('counter_id', counterData.id)
                counterDataForm.append('counter_day_data', counterData.day_val)
                counterDataForm.append('counter_night_data', counterData.night_val)
                counterDataForm.append('old_counter_day_data', day_oldCounterData)
                counterDataForm.append('old_counter_night_data', night_oldCounterData)
                counterDataForm.append('old_date_update', oldCounterDate)
                counterDataForm.append('type', type) 
            } else if ((counterData.day_val && !counterData.night_val) || (!counterData.day_val && counterData.night_val)){
                counterData.error = true
                counterData.message = 'Заполните оба поля дневные и ночные показания!'
                counterData.loading = false
            } else {
                counterData.loading = false
                return
            }
            if (counterData.loading) {
                var response = await put_electric_counter_data_by_counter_id(counterDataForm, this.account)
                counterData.loading = false
                this.resposneViewer(response, counterData)
                if (response.status === 'OK') {
                    this.updateViewCounter(index, response, counterData, oldCounterDate, simple_oldCounterData, day_oldCounterData, night_oldCounterData)
                }
            }
            
        },
    },
    computed : {
        electricRows () {
        const rows = []
        this.electricCounters.forEach((item, index) => {
            const row = Math. floor (index / 4) // 4 represents four rows, which can be changed at will
            if (!rows[row]) {
            rows[row] = []
            }
            rows[row].push(item)
        })
        return rows
        }
    },
    created () {
        this.electricCounters.forEach((item, index) => {
            this.electricInputs.push({
                id: item.id,
                simple_val: '',
                day_val: '',
                night_val: '',
                success: false,
                error: false,
                message: '',
                loading: false,
                simple_diff: '',
                day_diff: '',
                night_diff: ''
            })
        })
    },
})
</script>

<style scoped>
.counter-row {
    margin-bottom: 1em;
}
.card-header {
  display: flex;
  /*justify-content: space-between;*/
  align-items: center;
}
.electric-card-header-text {
    margin-left: 1rem;
}
.electric-counter-bg {
    background-color: #c6e2ff;
}
.electric-divider-color {
    background-color: black;
}
.card-data {
    text-align: right;
}
.el-row {
  margin-bottom: 0.3rem;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active до версии 2.1.8 */ {
  opacity: 0;
}
</style>