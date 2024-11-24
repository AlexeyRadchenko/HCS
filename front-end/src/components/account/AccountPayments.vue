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
        <el-row justify="center" ><el-col :span="12" class="pay-doc-header" style="margin-bottom: 1rem;"><h2>Платежный документ (счет) на оплату услуг за {{ monthName }} {{ year }}</h2></el-col></el-row>
        <el-row :gutter="20">
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
                <el-row class="pay-doc-header"><el-col><h4>Идентификатор платежного документа</h4></el-col></el-row>
                <el-row class="pay-doc-header"><el-col><h4>Раздел 2. Информация для внесения платы получателю платежа</h4></el-col></el-row>
                <el-row>
                    <el-col :span="24">
                        <partPayInfo :organisation="org" :account="account" :accSummary="accountSummary" :payer="FIO" :payerAddress="address" />
                    </el-col>
                </el-row>    
            </el-col>
        </el-row>
        <el-row :gutter="20" style="margin-top: 1rem;">
            <el-col :span="16">
                <el-row class="pay-doc-header"><el-col><h4>Раздел 3. Расчет размера платы за содержание и ремонт жилого помещения и коммунальные услуги</h4></el-col></el-row>
                <el-row>
                    <el-col :span="24">
                       
                    </el-col>
                </el-row>
            </el-col>
            <el-col :span="8">
                <el-row class="pay-doc-header"><el-col><h4>Раздел 4. Справочная информация</h4></el-col></el-row>
                <el-row>
                    <el-col :span="24">
              
                    </el-col>
                </el-row>    
            </el-col>
        </el-row>    
        {{ account }}
        {{ this.accAuthStore.getAccountData }}
    </div>    
</template>

<script>
import { defineComponent, onMounted } from 'vue'
import { useAccountAuthStore } from '../../storage/accountAuthService'
import PartInfo from './paymentParts/PartInfo.vue'
import partPayInfo from './paymentParts/partPayInfo.vue'
import moment from 'moment/dist/moment'
import ru from 'moment/dist/locale/ru'

export default defineComponent({
    components: {
        PartInfo,
        partPayInfo
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
        },
        account () {
            if (!this.dataLoading) {
                return this.accAuthStore.getAccountData.account
            }
            return ''
        },
        FIO () {
            if (!this.dataLoading) {
                return {
                    'name': this.accAuthStore.getAccountData.name,
                    'middle_name': this.accAuthStore.getAccountData.second_name,
                    'last_name': this.accAuthStore.getAccountData.surname,
                }
            }
            return {}
        }
    },
    async mounted() {
        var month = 'get_last_payment_month_by_account()'
        var calculateInfo = 'get_calculate_info_by_account_and_date()'
    }
})
</script>

<style scoped>
.pay-doc-header {
    color:black;
}
</style>