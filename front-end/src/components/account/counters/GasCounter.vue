<template>
    <div>
        <el-row>
            <el-col :span="24">
                <el-divider content-position="left"><h2>Газовые счётчики</h2></el-divider>
            </el-col>
        </el-row>
        <el-row :gutter="12" v-for="(row, index) in gasRows" :key="index" class="counter-row">
            <el-col :span="6" v-for="(item, innerindex) in row" :key="item.id" >
            <el-card shadow="always" class="gas-counter-bg">
                <template #header>
                    <div class="card-header">
                        <font-awesome-icon :icon="['fas', 'fire-alt']" size="1x" />
                        <span class="gas-card-header-text"><h3>{{ 'Счетчик газа № ' + item.serial_number }}</h3></span>
                    </div>
                </template>
                <el-row>
                    <el-col :span="14"><h4>Дата последней поверки:</h4></el-col><el-col :span="10" class="card-data">{{ dateCounterView(item.setup_date) }}</el-col>
                </el-row>
                <el-row>
                    <el-col :span="14"><h4>Дата предыдущих показаний:</h4></el-col><el-col :span="10" class="card-data">{{ dateCounterView(item.last_date_update) }}</el-col>
                </el-row>
                <el-row>
                    <el-col :span="14"><h4>Прошлые показания:</h4></el-col><el-col :span="10" class="card-data">{{ parseFloat(item.old_data).toFixed(3) }} м<sup>3</sup></el-col>
                </el-row>
                <el-divider border-style="dashed" class="gas-divider-color" />
                <el-row>
                    <el-col :span="14"><h4>Дата текущих показаний:</h4></el-col><el-col :span="10" class="card-data">{{ dateCounterView(item.date_update) }}</el-col>
                </el-row>
                <el-row>
                    <el-col :span="14"><h4>Текущие показания:</h4></el-col><el-col :span="10" class="card-data">{{ parseFloat(item.data).toFixed(3) }} м<sup>3</sup></el-col>
                </el-row>
                <el-divider border-style="dashed" class="gas-divider-color" />
                <el-row>
                    <el-col :span="14"><h4>Текущий расход:</h4></el-col><el-col :span="10" class="card-data">{{ parseFloat(item.diff).toFixed(3) }} м<sup>3</sup></el-col>
                </el-row>
                <el-row>
                    <el-col :span="14">
                        <el-input
                        v-model="gasInputs[innerindex].val"
                        placeholder="000,000"
                        size="large"
                        v-mask="gasInputMasks"
                        @keyup.enter="sendDataGasCounter(gasInputs[innerindex], item.old_data, item.date_update, innerindex)"
                        />
                    </el-col>
                    <el-col :span="2">
                        <el-popover
                            placement="top-start"
                            title="Подсказка"
                            :width="400"
                            trigger="hover"
                            content="Вводите все числа подряд. Например на счетчике 4.000 или 134.423, то нажимайте (4000) или (134423).
                            Точка поставиться сама !!!"
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
                        @click="sendDataGasCounter(gasInputs[innerindex], item.old_data, item.date_update, innerindex)"
                        :loading="gasInputs[innerindex].loading">Записать</el-button>
                    </el-col>
                </el-row>
                <el-row style="height: 1.9rem;">
                    <el-col :span="24">
                        <el-alert
                         :title="gasInputs[innerindex].message"
                         type="success"
                         show-icon
                         v-if="gasInputs[innerindex].success"
                         @close="alertsClose(gasInputs[innerindex])" /> 
                        <el-alert
                        v-show="gasInputs[innerindex].error"
                        :title="gasInputs[innerindex].message" 
                        type="error"
                        show-icon v-if="gasInputs[innerindex].error"
                        @close="alertsClose(gasInputs[innerindex])" />
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
import { put_gas_counter_data_by_counter_id } from '../../../http/account-http-common'

export default defineComponent({
    setup() {
        moment.updateLocale('ru', ru)
        return { moment }
    },
    data () {
        return {
            gasInputs: [],
            gasInputMasks: [
                '#.#', '#.##', '#.###', '##.###', '###.###', '####.###', '#####.###'
            ],
        }
    },
    props: {
        gasCounters: Array,
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
                this.gasCounters[index].data = dataNow
                this.gasCounters[index].date_update = 'now'
                this.gasCounters[index].old_data = oldData
                this.gasCounters[index].last_date_update = oldDate
                this.gasCounters[index].diff = response.difference
            }else{
                this.gasCounters[index].data = dataNow
                this.gasCounters[index].date_update = 'now'
                this.gasCounters[index].diff = response.difference
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
        async sendDataGasCounter (counterData, oldCounterData, oldCounterDate, index) {
            if (!counterData.val) {
                return
            }
            counterData.loading = true
            var counterDataForm = new FormData()
            counterDataForm.append('counter_id', counterData.id)
            counterDataForm.append('counter_data', counterData.val)
            counterDataForm.append('old_counter_data', oldCounterData)
            counterDataForm.append('old_date_update', oldCounterDate)
            var response = await put_gas_counter_data_by_counter_id(counterDataForm, this.account)
            counterData.loading = false
            this.resposneViewer(response, counterData)
            if (response.status === 'OK') {
                this.updateViewCounter(index, response, counterData.val, oldCounterData, oldCounterDate)
            }
            
        },
    },
    computed : {
        gasRows () {
        const rows = []
        this.gasCounters.forEach((item, index) => {
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
        this.gasCounters.forEach((item, index) => {
            this.gasInputs.push({
                id: item.id,
                val: '',
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
.gas-card-header-text {
    margin-left: 1rem;
}
.gas-counter-bg {
    background-color: #c6e2ff;
}
.gas-divider-color {
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