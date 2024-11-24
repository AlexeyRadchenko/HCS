<template>
    <el-form
        :label-position="labelPosition"
        label-width="100px"
        :model="formDataModal"
        style="width 50%;"
    >
            <el-row :gutter="5">
                <el-col :span="8">
                    <el-form-item label="Имя" >
                    <el-input v-model="formDataModal.name"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">    
                    <el-form-item label="Отчество">
                    <el-input v-model="formDataModal.second_name"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">   
                    <el-form-item label="Фамилия">
                    <el-input v-model="formDataModal.surname"></el-input>
                    </el-form-item>
                </el-col>    
            </el-row>
            <el-row :gutter="5">
                <el-col :span="8">
                    <el-form-item label="Мобильный телефон" >
                    <el-input v-model="formDataModal.mobile_phones"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">    
                    <el-form-item label="Домашний телефон">
                    <el-input v-model="formDataModal.home_phones"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">   
                    <el-form-item label="Рабочий телефон">
                    <el-input v-model="formDataModal.work_phones"></el-input>
                    </el-form-item>
                </el-col>     
            </el-row>
            <el-row :gutter="5">
                <el-col :span="8">
                    <el-form-item label="Дом">
                        <el-select v-model="formDataModal.street_house" filterable placeholder="Адрес" style="width:100%;">
                            <el-option
                            v-for="item in addressesForModal"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                            >
                            </el-option>
                        </el-select>
                    </el-form-item>    
                </el-col>
                <el-col :span="8">    
                    <el-form-item label="Подъезд">
                    <el-input v-model="formDataModal.entrance"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">   
                    <el-form-item label="Квартира">
                    <el-input v-model="formDataModal.appartment"></el-input>
                    </el-form-item>
                </el-col>         
            </el-row>
            <el-row :gutter="5">
                <el-col :span="8">    
                    <el-form-item label="Доля имущества">
                    <el-select v-model="formDataModal.part_own" filterable placeholder="Доля" style="width:100%;">
                        <el-option
                        v-for="item in ownParts"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value"
                        >
                        </el-option>
                    </el-select>
                    </el-form-item>    
                </el-col>
                 <el-col :span="16">
                    <el-form-item label="Примечание">
                    <el-input v-model="formDataModal.note" :rows="1" type="textarea"></el-input>
                    </el-form-item>
                </el-col>  
            </el-row>       
    </el-form>
</template>

<script>
import { handleModalAddresses } from '../utils/utils';

export default {
    setup() {
        
    },
    data () {
        return {
            labelPosition: 'top',
            ownParts:[
                {
                lable: 'Владелец',
                value: '1'
                },
                {
                lable: '1/2',
                value: '1/2'    
                },
                {
                lable: '1/3',
                value: '1/3'    
                },
                {
                lable: '1/4',
                value: '1/4'    
                },
                {
                lable: '1/5',
                value: '1/5'    
                },
                {
                lable: '1/6',
                value: '1/6'    
                },
                {
                lable: '1/7',
                value: '1/7'    
                },
                {
                lable: '1/8',
                value: '1/8'    
                },
                {
                lable: '1/9',
                value: '1/9'    
                },
                {
                lable: '1/10',
                value: '1/10'    
                },
            ]
        }
    },
    props: {
        modalKomfAddresses: Array,
        modalJKSAddresses: Array,
        formDataModal: Object,
    },
    methods: {

    },
    computed: {
        addressesForModal () {
            var komf_addresses_list_for_select = handleModalAddresses (this.modalKomfAddresses)
            var jks_addresses_list_for_select = handleModalAddresses (this.modalJKSAddresses)
            return komf_addresses_list_for_select.concat(jks_addresses_list_for_select)
        }
    }
}
</script>

<style scoped>
.form-item-style {
    width: 1.2em;
}
</style>
