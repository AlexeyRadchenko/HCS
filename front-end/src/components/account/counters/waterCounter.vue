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
                        <span><h3>{{ item.type === 'cold' ? 'Счетчик холодной воды № ' + item.serial_number : 'Счетчик горячей воды № ' + item.serial_number }}</h3></span>
                    </div>
                </template>
                <el-row>
                    <el-col :span="14"><h4>Дата последней поверки:</h4></el-col><el-col :span="10" class="card-data">{{ dateCounterView(item.setup_date) }}</el-col>
                </el-row>
                <el-row>
                    <el-col :span="14"><h4>Дата последних показаний:</h4></el-col><el-col :span="10" class="card-data">{{ dateCounterView(item.date_update) }}</el-col>
                </el-row>
                <el-row>
                    <el-col :span="14"><h4>Последние показания:</h4></el-col><el-col :span="10" class="card-data">{{ item.data }} м<sup>3</sup></el-col>
                </el-row>
                <el-row>
                    <el-col :span="14"><h4>Дата предыдущих показаний:</h4></el-col><el-col :span="10" class="card-data">{{ dateCounterView(item.last_date_update) }}</el-col>
                </el-row>
                <el-row>
                    <el-col :span="14"><h4>Прошлые показания:</h4></el-col><el-col :span="10" class="card-data">{{ item.data }} м<sup>3</sup></el-col>
                </el-row>
                <el-row>
                    <el-col :span="16">
                        <el-input
                        v-model="waterInputs[innerindex].val"
                        placeholder="000,000"
                        size="large"
                        :formatter="(value) => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')"
                        :parser="(value) => value.replace(/\$\s?|(,*)/g, '')"
                    />
                    </el-col>
                    <el-col :span="8" class="card-data"><el-button size="large" @click="sendDataWaterCounter(waterInputs[innerindex])">Записать</el-button></el-col>
                </el-row>
                <el-row>
                    <el-col :span="24">
                        <el-alert title="success alert" type="success" show-icon />
                        <el-alert title="error alert" type="error" show-icon />
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
        }
    },
    props: {
        waterCounters: Array,
    },
    methods: {
        dateCounterView (date) {
            return moment(date).format('L')
        },
        sendDataWaterCounter (counterData) {
            console.log(counterData.id, counterData.val)
        }
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
            this.waterInputs.push({id: item.id, val: '' })
        })
    }
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
  justify-content: space-between;
  align-items: center;
}
.card-data {
    text-align: right;
}
.el-row {
  margin-bottom: 0.3rem;
}
</style>