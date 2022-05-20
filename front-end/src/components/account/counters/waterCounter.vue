<template>
    <div>
        <el-row>
            <el-col :span="24">
                <el-divider content-position="left"><h2>Водосчётчики</h2></el-divider>
            </el-col>
        </el-row>
        <el-row :gutter="12" v-for="(row, index) in waterRows" :key="index" class="counter-row">
            <el-col :span="6" v-for="(item, innerindex) in row" :key="item.id" >
            <el-card shadow="always" :class="[item.type === 'cold' ? coldWaterClass : hotWaterClass]">
                <template #header>
                    <div class="card-header">
                        <font-awesome-icon :icon="['fas', 'water']" size="1x" />
                        <span class="water-card-header-text" ><h3>{{ item.type === 'cold' ? 'Счетчик холодной воды № ' + item.serial_number : 'Счетчик горячей воды № ' + item.serial_number }}</h3></span>
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
                <el-divider border-style="dashed" />
                <el-row>
                    <el-col :span="14"><h4>Дата текущих показаний:</h4></el-col><el-col :span="10" class="card-data">{{ dateCounterView(item.date_update) }}</el-col>
                </el-row>
                <el-row>
                    <el-col :span="14"><h4>Текущие показания:</h4></el-col><el-col :span="10" class="card-data">{{ parseFloat(item.data).toFixed(3) }} м<sup>3</sup></el-col>
                </el-row>
                <el-divider border-style="dashed" />
                <el-row>
                    <el-col :span="14"><h4>Текущий расход:</h4></el-col><el-col :span="10" class="card-data">{{ parseFloat(item.diff).toFixed(3) }} м<sup>3</sup></el-col>
                </el-row>
                <el-row>
                    <el-col :span="14">
                        <el-input
                        v-model="waterInputs[innerindex].val"
                        placeholder="000,000"
                        size="large"
                        v-mask="waterInputMasks"
                        @keyup.enter="sendDataWaterCounter(waterInputs[innerindex], item.old_data, item.date_update, innerindex)"
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
                        @click="sendDataWaterCounter(waterInputs[innerindex], item.old_data, item.date_update, innerindex)"
                        :loading="waterInputs[innerindex].loading">Записать</el-button>
                    </el-col>
                </el-row>
                <el-row style="height: 1.9rem;">
                    <el-col :span="24">
                        <el-alert
                         :title="waterInputs[innerindex].message"
                         type="success"
                         show-icon
                         v-if="waterInputs[innerindex].success"
                         @close="alertsClose(waterInputs[innerindex])" /> 
                        <el-alert
                        v-show="waterInputs[innerindex].error"
                        :title="waterInputs[innerindex].message" 
                        type="error"
                        show-icon v-if="waterInputs[innerindex].error"
                        @close="alertsClose(waterInputs[innerindex])" />
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
import { put_water_counter_data_by_counter_id } from '../../../http/account-http-common'

export default defineComponent({
    setup() {
        moment.updateLocale('ru', ru)
        return { moment }
    },
    data () {
        return {
            coldWaterClass: 'coldWater',
            hotWaterClass: 'hotWater',
            waterInputs: [],
            waterInputMasks: [
                '#.#', '#.##', '#.###', '##.###', '###.###', '####.###', '#####.###'
            ],
        }
    },
    props: {
        waterCounters: Array,
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
                this.waterCounters[index].data = dataNow
                this.waterCounters[index].date_update = 'now'
                this.waterCounters[index].old_data = oldData
                this.waterCounters[index].last_date_update = oldDate
                this.waterCounters[index].diff = response.difference
            }else{
                this.waterCounters[index].data = dataNow
                this.waterCounters[index].date_update = 'now'
                this.waterCounters[index].diff = response.difference
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
        async sendDataWaterCounter (counterData, oldCounterData, oldCounterDate, index) {
            if (!counterData.val) {
                return
            }
            counterData.loading = true
            var counterDataForm = new FormData()
            counterDataForm.append('counter_id', counterData.id)
            counterDataForm.append('counter_data', counterData.val)
            counterDataForm.append('old_counter_data', oldCounterData)
            counterDataForm.append('old_date_update', oldCounterDate)
            var response = await put_water_counter_data_by_counter_id(counterDataForm, this.account)
            counterData.loading = false
            this.resposneViewer(response, counterData)
            if (response.status === 'OK') {
                this.updateViewCounter(index, response, counterData.val, oldCounterData, oldCounterDate)
            }
            
        },
    },
    computed : {
        waterRows () {
        const rows = []
        this.waterCounters.forEach((item, index) => {
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
        this.waterCounters.forEach((item, index) => {
            this.waterInputs.push({
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
.coldWater {
    background-color: #409EFF;
}
.hotWater {
    background-color: #F56C6C;
}
.counter-row {
    margin-bottom: 1em;
}
.card-header {
  display: flex;
  /*justify-content: space-between;*/
  align-items: center;
}
.water-card-header-text {
    margin-left: 1rem;
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