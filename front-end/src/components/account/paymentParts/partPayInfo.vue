<template>
    <div class="part-two-border-block">
        <el-row>
            <el-col :span="16">
                <el-row>
                    <el-col :span="24"><h3 class="part-two-str-tab">Получатель {{ organisation.full_name }}</h3></el-col>
                </el-row>
                <el-row>
                    <el-col :span="5"><h3 class="part-two-str-tab">Р/с</h3></el-col><el-col :span="18"><h3 class="part-two-str">{{ organisation.r_s }}</h3></el-col>
                </el-row>
                <el-row>
                    <el-col :span="5"><h3 class="part-two-str-tab">Банк</h3></el-col><el-col :span="19"><h3 class="part-two-str">{{ organisation.bank }}</h3></el-col>
                </el-row>
                <el-row>
                    <el-col :span="10">
                        <el-row>
                            <el-col :span="12"><h3 class="part-two-str-tab">БИК</h3></el-col><el-col :span="12"><h3 class="part-two-str">{{ organisation.bik }}</h3></el-col>
                        </el-row>
                    </el-col>
                    <el-col :span="7">
                        <el-row justify="end">
                            <el-col :span="7"><h3 class="part-two-str-tab">ИНН</h3></el-col><el-col :span="17"><h3 class="part-two-str-tab">{{ organisation.inn }}</h3></el-col>
                        </el-row>
                    </el-col>
                    <el-col :span="7">
                        <el-row>
                            <el-col :span="8"><h3 class="part-two-str-tab">КПП</h3></el-col><el-col :span="16"><h3 class="part-two-str-tab">{{ organisation.kpp }}</h3></el-col>
                        </el-row>
                    </el-col>
                </el-row>
               <el-row>
                    <el-col :span="5"><h3 class="part-two-str-tab">Корр. счет</h3></el-col><el-col :span="19"><h3 class="part-two-str">{{ organisation.korr_acc }}</h3></el-col>
                </el-row>
                <el-row>
                    <el-col :span="12"><h3 class="part-two-str-tab part-two-bold-str">Лицевой счет плательщика</h3></el-col><el-col :span="12"><h3 class="part-two-str part-two-bold-str">{{ account }}</h3></el-col>
                </el-row>
                <el-row>
                    <el-col :span="12"><h3 class="part-two-str-tab part-two-bold-str">Сумма к оплате</h3></el-col><el-col :span="12"><h3 class="part-two-str part-two-bold-str">{{ accSummary.payment_sum }} руб.</h3></el-col>
                </el-row>
                <el-row  style="margin-top: 1rem;">
                    <el-col :span="16"><h3 class="part-two-str-tab">Задолженность на начало периода</h3></el-col><el-col :span="8"><h3 class="part-two-str">{{ accSummary.debt_start_period }} руб.</h3></el-col>
                </el-row>
                <el-row>
                    <el-col :span="16"><h3 class="part-two-str-tab">Начислено</h3></el-col><el-col :span="8"><h3 class="part-two-str">{{ accSummary.debt }} руб.</h3></el-col>
                </el-row>
                <el-row>
                    <el-col :span="16"><h3 class="part-two-str-tab">Оплачено</h3></el-col><el-col :span="8"><h3 class="part-two-str">{{ accSummary.paying }} руб.</h3></el-col>
                </el-row>
                <el-row>
                    <el-col :span="16"><h3 class="part-two-str-tab">Дата последней оплаты</h3></el-col><el-col :span="8"><h3 class="part-two-str">{{ datePayInfoView(accSummary.last_payment_date) }}</h3></el-col>
                </el-row>
                <el-row>
                    <el-col :span="16"><h3 class="part-two-str-tab">Задолженность на конец периода </h3></el-col><el-col :span="8"><h3 class="part-two-str">{{ accSummary.debt_end_period }} руб.</h3></el-col>
                </el-row>
                <el-row style="margin-bottom: 0.9rem;">
                    <el-col :span="16"><h3 class="part-two-str-tab">Итого к оплате</h3></el-col><el-col :span="8"><h3 class="part-two-str">{{ accSummary.ending_payment}} руб.</h3></el-col>
                </el-row>
            </el-col>
            <el-col :span="8">
                <div class="qr-code-pos">
                    <vue-qrcode :value="QRvalue" :options="{ width: 250 }"></vue-qrcode>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>

import { defineComponent } from 'vue'
import moment from 'moment/dist/moment'
import ru from 'moment/dist/locale/ru'
import VueQrcode from '@chenfengyuan/vue-qrcode';

export default defineComponent ({
    setup() {
        moment.updateLocale('ru', ru)
        return { moment }
    },
    data () {
        return {
        }
    },
    props: {
        organisation: Object,
        account: String,
        accSummary: Object,
        payer: Object,
        payerAddress: Object,
    },
    components: {
        'vue-qrcode': VueQrcode
    },
    methods: {
        datePayInfoView (date) {
            if (date === 'now') {
                return moment().format('L')
            }
            return moment(date).format('L')
        },
    },
    computed: {
        QRvalue () {
            const startOfMonth = moment(this.accSummary.last_payment_date).startOf('month').format('L')
            const bankName = String(this.organisation.bank).toUpperCase()
            let qr_value = 'ST00012|Name=' + this.organisation.qr_short_name + '|' +
                           'PersonalAcc=' + this.organisation.r_s + '|' +
                           'BankName=' + bankName + '|' +
                           'BIC=' + this.organisation.bik + '|' + 
                           'CorrespAcc=' + this.organisation.korr_acc + '|' + 
                           'Sum=' + this.accSummary.ending_payment + '|' + 
                           'PayeeINN=' + this.organisation.inn + '|' + 
                           'TaxPeriod=' + startOfMonth + '|' + 
                           'DocNo=' + this.account + '|' + 
                           'lastName=' + this.payer.last_name + '|' + 
                           'firstName=' + this.payer.name + '|' + 
                           'middleName=' + this.payer.middle_name + '|' + 
                           'payerAddress=' + this.payerAddress.street + ',' + this.payerAddress.house + ',  ' +  this.payerAddress.appartment + '|' + 
                           'persAcc=' + this.account               
            return qr_value
        }, 
    },

})
</script>

<style scss>
.part-two-border-block {
    border: 1px solid black;
}
.part-two-str {
    color:black;
}
.part-two-str-tab {
    color:black;
    margin-left: 1rem;
}
.part-two-bold-str {
    font-weight: bold;
}
.qr-code-pos {
    margin-top: 3rem;
    margin-left: 1.5rem;
}
</style>