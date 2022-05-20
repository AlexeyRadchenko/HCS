<template>
    <div>
        <el-row>
            <el-col :span="24">
                <el-divider content-position="left"><h2>Электросчетчики</h2></el-divider>
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
                <el-divider border-style="dashed" class="electric-divider-color" />
                <el-row v-if="item.type === 'single'">
                    <el-col :span="14"><h4>Текущий расход:</h4></el-col><el-col :span="10" class="card-data">{{ item.simple_diff }} кВт/ч</el-col>
                </el-row>
                <el-row v-if="item.type === 'double'">
                    <el-col :span="14"><h4>Текущий расход день:</h4></el-col><el-col :span="10" class="card-data">{{ item.day_diff }} кВт/ч</el-col>
                </el-row>
                <el-row v-if="item.type === 'double'">
                    <el-col :span="14"><h4>Текущий расход ночь:</h4></el-col><el-col :span="10" class="card-data">{{ item.night_diff }} кВт/ч</el-col>
                </el-row>
                <el-row v-if="item.type === 'single'">
                    <el-col :span="14">
                        <el-input
                        v-model="electricInputs[innerindex].simple_val"
                        placeholder="0"
                        size="large"
                        v-mask="electricInputMasks"
                        @keyup.enter="sendDataElectricCounter(electricInputs[innerindex], item.old_data, item.date_update, innerindex)"
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
                        @click="sendDataElectricCounter(electricInputs[innerindex], item.old_data, item.date_update, innerindex)"
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
                        @keyup.enter="sendDataElectricCounter(electricInputs[innerindex], item.old_data, item.date_update, innerindex)"
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
                        @keyup.enter="sendDataElectricCounter(electricInputs[innerindex], item.old_data, item.date_update, innerindex)"
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
                    <el-col :span="8" class="card-data">
                        <el-button
                        size="large"
                        @click="sendDataElectricCounter(electricInputs[innerindex], item.old_data, item.date_update, innerindex)"
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
        updateViewCounter (index, response, dataNow, oldData, oldDate) {
            console.log(response)
            if (response.exch) {
                this.electricCounters[index].data = dataNow
                this.electricCounters[index].date_update = 'now'
                this.electricCounters[index].old_data = oldData
                this.electricCounters[index].last_date_update = oldDate
                this.electricCounters[index].diff = response.difference
            }else{
                this.electricCounters[index].data = dataNow
                this.electricCounters[index].date_update = 'now'
                this.electricCounters[index].diff = response.difference
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
        async sendDataElectricCounter (counterData, oldCounterData, oldCounterDate, index) {
            if (!counterData.val) {
                return
            }
            counterData.loading = true
            var counterDataForm = new FormData()
            counterDataForm.append('counter_id', counterData.id)
            counterDataForm.append('counter_data', counterData.val)
            counterDataForm.append('old_counter_data', oldCounterData)
            counterDataForm.append('old_date_update', oldCounterDate)
            var response = await put_electric_counter_data_by_counter_id(counterDataForm, this.account)
            counterData.loading = false
            this.resposneViewer(response, counterData)
            if (response.status === 'OK') {
                this.updateViewCounter(index, response, counterData.val, oldCounterData, oldCounterDate)
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