<template>
    <div class="part-one-border-block">
        <el-row>
            <el-col :span="24"><h3 class="part-one-str">Плательщик:</h3></el-col>
        </el-row>
        <el-row>
            <el-col :span="24"><h3 class="part-one-str-tab">За {{ month }} {{ year }} (расчетный период)</h3></el-col>
        </el-row>
        <el-row>
            <el-col :span="24"><h3 class="part-one-str-tab">Ф.И.О. (наименование) собственника/нанимателя: (не указывается)</h3></el-col>
        </el-row>
        <el-row>
            <el-col :span="24"><h3 class="part-one-str-tab">Адрес помещения {{ address.street }}, {{ address.house }}, {{ address.appartment }}</h3></el-col>
        </el-row>
        <el-row>
            <el-col :span="24"><h3 class="part-one-str-tab">Общая площадь лицевого счета: {{ accParams.living_square }}; Площадь жилих и нежилих помещений: {{ accParams.sum_square }}</h3></el-col>
        </el-row>
        <el-row>
            <el-col :span="24"><h3 class="part-one-str-tab">Количество проживающих: {{ accParams.living_quantity }}; Количество прописанных: {{ accParams.record_living_quantity }}</h3></el-col>
        </el-row>
        <el-row>
            <el-col :span="24"><h3 class="part-one-str">Исполнитель: </h3></el-col>
        </el-row>
        <el-row>
            <el-col :span="24"><h3 class="part-one-str-tab">Наименование/Ф.И.О: {{ organisation.full_name }}</h3></el-col>
        </el-row>
        <el-row>
            <el-col :span="24"><h3 class="part-one-str-tab">Адрес: {{ organisation.address }}</h3></el-col>
        </el-row>
        <el-row>
            <el-col :span="24"><h3 class="part-one-str-tab">Телефон: {{ organisation.phones }}; Диспетчерская служба: {{ organisation.dispatcher_phones }}; Сайт {{ organisation.site }}</h3></el-col>
        </el-row>
        <el-row>
            <el-col :span="12" :offset="6">
                <vue3-barcode value="001000010010322104763463" :height="50" />
            </el-col>
        </el-row>
    </div>
</template>

<script>
import Vue3Barcode from 'vue3-barcode'
import { defineComponent } from 'vue'

export default defineComponent ({
    setup() {
        
    },
    data () {
        return {
            
        }
    },
    props: {
        month: String,
        year: Number,
        address: Object,
        accParams: Object,
        organisation: Object,  
    },
    components: {
        'vue3-barcode': Vue3Barcode, //https://www.npmjs.com/package/vue3-barcode
    },
    methods: {
       
    },
    computed: {
    },

})
</script>

<style scss>

.part-one-border-block {
    border: 1px solid black;
}
.part-one-str {
    color:black;
}
.part-one-str-tab {
    color:black;
    margin-left: 1rem;
}
</style>