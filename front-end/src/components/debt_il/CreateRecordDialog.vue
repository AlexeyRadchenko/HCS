<template>
  <el-dialog v-model="dialogVisible" title="Создать запись" width="80%" :close-on-click-modal="false" draggable>
    <el-form
      ref="ruleFormRef"
      :model="ruleForm"
      :rules="rules"
      label-width="135px"
      :size="formSize"
      status-icon
    >
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="Адрес" required>
            <el-select v-model="ruleForm.street" prop="street" placeholder="Улица" style="width:100%;" >
              <el-option
                v-for="item in options_street"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>  
        </el-col>
        <el-col :span="4">
            <el-input v-model="ruleForm.home" placeholder="Дом"/>
        </el-col>
        <el-col :span="4">
            <el-input v-model="ruleForm.appartment" placeholder="Квартира" />
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="Собственность" prop="one_or_parts" required>
            <el-select v-model="ruleForm.one_or_parts" style="width:100%;" >
                <el-option
                  v-for="item in options_own"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="4">
            <el-select v-model="ruleForm.property_self" style="width:100%;" >
                <el-option
                  v-for="item in options_property_self"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
            </el-select>
        </el-col>
      </el-row>
      <el-divider />
      <el-row :gutter="20">
        <el-col :span="6">
          <el-form-item label="Номер исполнительного производства" required>
            <el-input v-model="ruleForm.il_number" placeholder="номер" style="width:100%; margin-top:2em;"/>
          </el-form-item>  
        </el-col>
        <el-col :span="4">
            <el-date-picker
              v-model="ruleForm.il_date"
              format="DD.MM.YYYY"
              type="date"
              label="дата и/л"
              placeholder="дата и/л"
              style="margin-top:2em;"
            />
        </el-col>
        <el-col :span="4">
            <el-date-picker
              v-model="ruleForm.start_exec_pross_date"
              format="DD.MM.YYYY"
              type="daterange"
              start-placeholder="Начальная дата"
              end-placeholder="Конечная дата"
              range-separator="до"
              label="период задолженности"
              placeholder="период задолженности"
              style="margin-top:2em;  height:3em;"
            />
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="4" :offset="2">
          <el-input v-model="ruleForm.sum_all_get" placeholder="взысканная сумма" style="width:100%; margin-top:2em; margin-left:0.5em;" />
        </el-col>
        <el-col :span="4">
          <el-input v-model="ruleForm.sum_not_yet_get" placeholder="остаток задолженности" style="width:100%; margin-top:2em;" />
        </el-col>
        <el-col :span="3">
          <el-input v-model="ruleForm.gov_tax" placeholder="сумма гос. пошлины" style="width:100%; margin-top:2em;" />
        </el-col>
        <el-col :span="3">
          <el-input v-model="ruleForm.gov_tax" placeholder="сумма долга" style="width:100%; margin-top:2em;" />
        </el-col>         
      </el-row>  
      <el-divider />
      <el-row>
        <el-col>
          <el-form-item
            v-for="(account, index) in ruleForm.accounts_il"
            :key="account.uuid"
            :label="'Должник ' + index"
            :prop="'accounts_il.' + index + '.surname'"
            :rules="{
              required: true,
              message: 'domain can not be null',
              trigger: 'blur',
            }"
          > <el-row :gutter="20">
              <el-col :span="6"><el-input v-model="account.surname" placeholder="Фамилия" /></el-col>
              <el-col :span="6"><el-input v-model="account.name" placeholder="Имя" /></el-col>
              <el-col :span="6"><el-input v-model="account.second_name" placeholder="Отчество" /></el-col>
              <el-col :span="6"><el-input v-model="account.account_number" placeholder="Лицевой счет" /></el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="6">
                <el-date-picker
                  v-model="account.passport_il.birth_date"
                  format="DD.MM.YYYY"
                  type="date"
                  label="Дата рождения"
                  placeholder="Дата рождения"
                  style="width:100%;"
                />
              </el-col>
              <el-col :span="6"><el-input v-model="account.passport_il.birth_place" placeholder="Место рождения" /></el-col>
              <el-col :span="6"><el-input v-model="account.passport_il.seria" placeholder="Серия паспорта" /></el-col>
              <el-col :span="6"><el-input v-model="account.passport_il.number" placeholder="Серия паспорта" /></el-col>
            </el-row>
            <el-button class="mt-2" @click.prevent="removeFIO(account)"
              >Delete</el-button
            >
          </el-form-item>
        </el-col>  
      </el-row>
      <el-row>
        <el-button @click="addAccount">Добавить Физ. лицо</el-button>
        <el-button @click="resetForm(formRef)">Reset</el-button>
      </el-row>  
    </el-form>        
        <template #footer>
        <span class="dialog-footer">
            <el-button @click="dialogVisible = false">Отмена</el-button>
            <el-button type="primary" @click="dialogVisible = false">
            Сохранить
            </el-button>
        </span>
        </template>
  </el-dialog>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'
//в onMound сгенерировать первый uuid в fuleForm.accounts_li.uuid
export default {
  expose: ['dialogVisible'],
  setup() {
    
  },
  data() {
    return {
      dialogVisible: false,
      formSize: 'default',
      ruleFormRef: {},
      ruleForm: {
        street: '',
        home:'',
        appartment: '',
        one_or_parts: true,
        property_self: true,
        il_number: '',
        il_date: '',
        gov_tax: '',
        sum_all_get: '',
        sum_not_yet_get: '',
        start_exec_pross_date: '',
        accounts_il: [
          {
            uuid: '',
            account_number: '',
            name: '',
            second_name: '',
            surname: '',
            passport_il: {
              id: 1,
              seria: '',
              number: '',
              who_take: '',
              when_take: '',
              squad_code: '',
              birth_date: '',
              birth_place: '',
              scan: ''
            } 
          }
        ],
      },
      rules: {
        street: [
          { required: true, message: 'Пожалуйста выберите улицу', trigger: 'blur' },
          { min: 3, max: 5, message: 'Length should be 3 to 5', trigger: 'blur' },
        ],
        region: [
          {
            required: true,
            message: 'Please select Activity zone',
            trigger: 'change',
          },
        ],
        count: [
          {
            required: true,
            message: 'Please select Activity count',
            trigger: 'change',
          },
        ],
        date1: [
          {
            type: 'date',
            required: true,
            message: 'Please pick a date',
            trigger: 'change',
          },
        ],
        date2: [
          {
            type: 'date',
            required: true,
            message: 'Please pick a time',
            trigger: 'change',
          },
        ],
        type: [
          {
            type: 'array',
            required: true,
            message: 'Please select at least one activity type',
            trigger: 'change',
          },
        ],
        resource: [
          {
            required: true,
            message: 'Please select activity resource',
            trigger: 'change',
          },
        ],
        desc: [
          { required: true, message: 'Please input activity form', trigger: 'blur' },
        ],
      },
      options_street:[
        {
        value: 'Строителей',
        label: 'Строителей'
        },
        {
        value: 'Володина',
        label: 'Володина'  
        },
        {
        value: 'Островского',
        label: 'Островского'  
        }
      ],
      options_own:[
        {
        value: true,
        label: 'Один собственник'
        },
        {
        value: false,
        label: 'Долевая'  
        }
      ],
      options_property_self:[
        {
        value: true,
        label: 'Частная'
        },
        {
        value: false,
        label: 'Соц. найм'  
        }
      ],
    }
  },
  methods:{
    async submitForm (formEl) {
      if (!formEl) return
      await formEl.validate((valid, fields) => {
        if (valid) {
          console.log('submit!')
        } else {
          console.log('error submit!', fields)
        }
      })
    },
    resetForm (formEl) {
      if (!formEl) return
      formEl.resetFields()
    },
    removeFIO (item) {
      const index = this.ruleForm.accounts_il.indexOf(item)
      if (index != -1) {
        this.ruleForm.accounts_il.splice(index, 1)
      }
    },
    addAccount () {
      let id = this.ruleForm.accounts_il.length + 1
      let uuid = uuidv4()
      this.ruleForm.accounts_il.push({
        uuid: uuid,
        account_number: '',
        name: '',
        second_name: '',
        surname: '',
        passport_il: {
          id: id,
          seria: "74 05",
          number: "111111",
          who_take: "ОВД администрации города Трехгорного Челябинской области",
          when_take: "2022-11-02T10:56:04.116Z",
          squad_code: "740-000",
          birth_date: "2022-11-02T10:56:04.116Z",
          birth_place: "г Златоуст-36 Челябинской области",
          scan: "string"
        }  
      })
    }
  },
  mounted() {
    this.ruleForm.accounts_il[0].uuid = uuidv4()
  }
}
</script>

<style>
form input:focus {
  width:100%;
}
.el-form-item__label {
  word-break: break-word;
}
</style>