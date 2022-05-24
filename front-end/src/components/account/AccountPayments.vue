<template>
    <div>
        <el-row>
            <el-col :span="24">
                <el-divider content-position="left"><h2>Платежные документы на оплату коммунальных услуг</h2></el-divider>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="3">
                <el-select v-model="month" class="m-2" size="large">
                    <el-option
                    v-for="item in months"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                    />
                </el-select>
            </el-col>
            <el-col :span="3">
                <el-select v-model="year" class="m-2" size="large">
                    <el-option
                    v-for="item in years"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                    />
                </el-select>
            </el-col>
        </el-row>"
        <el-row justify="center" ><el-col :span="12" class="pay-doc-header"><h2>Платежный документ (счет) на оплату услуг за {{ monthName }} {{ year }}</h2></el-col></el-row>
        <el-row>
            <el-col :span="12">
                <el-row class="pay-doc-header"><el-col><h4>Единый лицевой счет: {{ accountParams.etc }}</h4></el-col></el-row>
                <el-row class="pay-doc-header"><el-col><h4>Раздел 1. Сведения о плательщике и исполнителе услуг</h4></el-col></el-row>
                <el-row>
                    <el-col :span="24">
                        <PartInfo :month="monthName" :year="year" :address="address" :accParams="accountParams" :organisation="org" />
                    </el-col>
                </el-row>
            </el-col>
            <el-col :span="12">
                
            </el-col>
        </el-row>
        {{ this.accAuthStore.getAccountData }}
    </div>    
</template>

<script>
import { defineComponent } from 'vue'
import { useAccountAuthStore } from '../../storage/accountAuthService'
import PartInfo from './paymentParts/PartInfo.vue'
import moment from 'moment/dist/moment'
import ru from 'moment/dist/locale/ru'

export default defineComponent({
    components: {
        PartInfo,
    },
    setup() {
        const accAuthStore = useAccountAuthStore()
        moment.updateLocale('ru', ru)

        return { accAuthStore, moment }
    },
    data () {
        return {
            month: '0' +  (moment().month() + 1),
            year: moment().year(),
            months: [
                {
                    value: '01',
                    label: 'Январь',
                },
                {
                    value: '02',
                    label: 'Февраль',
                },
                {
                    value: '03',
                    label: 'Март',
                },
                {
                    value: '04',
                    label: 'Апрель',
                },
                {
                    value: '05',
                    label: 'Май',
                },
                {
                    value: '06',
                    label: 'Июнь',
                },
                {
                    value: '07',
                    label: 'Июль',
                },
                {
                    value: '08',
                    label: 'Август',
                },
                {
                    value: '09',
                    label: 'Сентябрь',
                },
                {
                    value: '10',
                    label: 'Октябрь',
                },
                {
                    value: '11',
                    label: 'Ноябрь',
                },
                {
                    value: '12',
                    label: 'Декабрь',
                },

            ],
            years: [
                {
                    value: '2022',
                    label: '2022',
                },
            ],
        }
    },
    props: {
        dataLoading: Boolean
    },
    computed: {
        accountParams () {
            if (!this.dataLoading) {
            return this.accAuthStore.getAccountData.account_params
            }
            return {}
        },
        accountSummary () {
            if (!this.dataLoading) {
            return this.accAuthStore.getAccountData.account_summary
            }
            return {}
        },
        monthName () {
            return this.months[parseInt(this.month) - 1].label
        },
        address () {
            if (!this.dataLoading) {
                return this.accAuthStore.getAccountData.address
            }
            return {}
        },
        org () {
            if (!this.dataLoading) {
                return this.accAuthStore.getAccountOrganisationData
            }
            return {}
        }
    },   
})
</script>

<style scoped>
.pay-doc-header {
    color:black;
}
</style>