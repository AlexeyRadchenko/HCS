<template>
    <el-form
        :label-position="labelPosition"
        label-width="100px"
        :model="formContactEditCreate"
        style="width 50%;"
    >
            <el-row :gutter="5">
                <el-col :span="8">
                    <el-form-item label="Имя" >
                    <el-input v-model="formContactEditCreate.name"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">    
                    <el-form-item label="Отчество">
                    <el-input v-model="formContactEditCreate.second_name"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">   
                    <el-form-item label="Фамилия">
                    <el-input v-model="formContactEditCreate.surname"></el-input>
                    </el-form-item>
                </el-col>    
            </el-row>
            <el-row :gutter="5">
                <el-col :span="8">
                    <el-form-item label="Мобильный телефон" >
                    <el-input v-model="formContactEditCreate.mobile_phones"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">    
                    <el-form-item label="Домашний телефон">
                    <el-input v-model="formContactEditCreate.home_phones"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">   
                    <el-form-item label="Рабочий телефон">
                    <el-input v-model="formContactEditCreate.work_phones"></el-input>
                    </el-form-item>
                </el-col>     
            </el-row>
            <el-row :gutter="5">
                <el-col :span="8">
                    <el-form-item label="Адрес">
                        <el-select v-model="formContactEditCreate.address" filterable placeholder="Адрес" style="width:100%;">
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
                    <el-form-item label="Электронная почта">
                    <el-input v-model="formContactEditCreate.emails"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="8">   
                    <el-form-item label="Примечание">
                    <el-input v-model="formContactEditCreate.work_phones"></el-input>
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
            formContactEditCreate: {
                name: '',
                second_name: '',
                surname: '',
                address: '',
                mobile_phones: '',
                home_phones: '',
                work_phones: '',
                emails: '',
            },
        }
    },
    props: {
        modalKomfAddresses: Array,
        modalJKSAddresses: Array
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
