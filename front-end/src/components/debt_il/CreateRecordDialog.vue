<template>
  <el-dialog v-model="dialogVisible" title="Создать запись" width="80%" :close-on-click-modal="false" draggable>
    <el-form
      ref="ruleFormRef"
      :model="ruleForm"
      :rules="rules"
      label-width="auto"
      :size="formSize"
      status-icon
      :validate-on-rule-change="false"
    >
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="Адрес" prop="street" required>
            <el-select v-model="ruleForm.street" placeholder="Улица" style="width:100%;" >
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
          <el-form-item prop="home" required >
            <el-input v-model="ruleForm.home" placeholder="Дом" />
          </el-form-item>  
        </el-col>
        <el-col :span="4">
          <el-form-item prop="appartment" required >
            <el-input v-model="ruleForm.appartment" placeholder="Квартира" />
          </el-form-item>  
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
          <el-form-item  prop="property_self" required>
            <el-select v-model="ruleForm.property_self" style="width:100%;" >
                <el-option
                  v-for="item in options_property_self"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
            </el-select>
          </el-form-item>  
        </el-col>
      </el-row>
      <el-divider />
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="Номер исполнительного производства" prop="il_number" label-width="auto" required>
            <el-input v-model="ruleForm.il_number" placeholder="номер" style="width:100%; margin-top:2em;"/>
          </el-form-item>  
        </el-col>
        <el-col :span="4">
          <el-form-item  prop="il_date" required>
            <el-date-picker
              v-model="ruleForm.il_date"
              format="DD.MM.YYYY"
              type="date"
              label="дата и/л"
              placeholder="дата и/л"
              style="margin-top:2em;"
            />
          </el-form-item>  
        </el-col>
        <el-col :span="6">
          <el-form-item  prop="period">
            <el-date-picker
              v-model="ruleForm.period"
              format="DD.MM.YYYY"
              type="daterange"
              start-placeholder="Начальная дата"
              end-placeholder="Конечная дата"
              range-separator="до"
              label="период задолженности"
              placeholder="период задолженности"
              style="margin-top:2em;  height:3em;"
            />
          </el-form-item>  
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item prop="sum_all_get" style="margin-left:18.7em;">
            <el-input v-model="ruleForm.sum_all_get" placeholder="взысканная сумма" style="width:100%; margin-top:2em; margin-left:0.5em;" />
          </el-form-item>  
        </el-col>
        <el-col :span="4">
          <el-form-item prop="sum_not_yet_get" >
            <el-input v-model="ruleForm.sum_not_yet_get" placeholder="остаток задолженности" style="width:100%; margin-top:2em;" />
          </el-form-item>  
        </el-col>
        <el-col :span="3">
          <el-form-item prop="gov_tax" >
            <el-input v-model="ruleForm.gov_tax" placeholder="сумма гос. пошлины" style="width:100%; margin-top:2em;" />
          </el-form-item>  
        </el-col>
        <el-col :span="3">
          <el-form-item prop="debt_sum_il" >
            <el-input v-model="ruleForm.debt_sum_il" placeholder="сумма долга" style="width:100%; margin-top:2em;" />
          </el-form-item>  
        </el-col>         
      </el-row>  
      <el-divider />
      <el-row
        v-for="(account, index) in ruleForm.accounts_il"
        :key="index"
      >
        <el-col :span="24">
          <el-row :gutter="20">
            <el-col :span="10">
              <el-form-item
                :label="'Должник ' + index"
                :prop="'accounts_il.' + index +'.surname'"
                :rules="[{ type: 'string', required: true, message: 'Пожалуйста укажите фамилию', trigger: 'blur',  }]"
                >
                <el-input v-model="account.surname" placeholder="Фамилия" required />
              </el-form-item>
            </el-col>     
            <el-col :span="6">
              <el-form-item
                :prop="'accounts_il.' + index +'.name'"
                :rules="[{ type: 'string', required: true, message: 'Пожалуйста укажите имя', trigger: 'blur',  }]"
              >
              <el-input v-model="account.name" placeholder="Имя" />
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item>
                <el-input v-model="account.second_name" placeholder="Отчество" /> 
              </el-form-item>  
            </el-col>
            <el-col :span="4">
              <el-form-item>
                <el-input v-model="account.account_number" placeholder="Лицевой счет" />
              </el-form-item>   
            </el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top:1em;">
              <el-col :span="4" :offset="4">
                <el-form-item style="margin-left:1.35em;">
                  <el-date-picker
                    v-model="account.passport_il.birth_date"
                    format="DD.MM.YYYY"
                    type="date"
                    label="Дата рождения"
                    placeholder="Дата рождения"
          
                  />
                </el-form-item>   
              </el-col> 
            <el-col :span="6">
              <el-form-item>
                <el-input v-model="account.passport_il.birth_place" placeholder="Место рождения" />
              </el-form-item>  
            </el-col>
            <el-col :span="4">
              <el-form-item>
                <el-input v-model="account.passport_il.serial" placeholder="Серия паспорта" />
              </el-form-item>  
            </el-col>    
            <el-col :span="4">
              <el-form-item>
                <el-input v-model="account.passport_il.number" placeholder="Номер паспорта" />
              </el-form-item>  
            </el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top:1em;">
            <el-col :span="4" :offset="4">
              <el-form-item style="margin-left:1.35em;">
                <el-date-picker
                  v-model="account.passport_il.when_take"
                  format="DD.MM.YYYY"
                  type="date"
                  label="Когда выдан"
                  placeholder="Когда выдан"
                  class="acc-datapicker"
                />
              </el-form-item>  
            </el-col>
            <el-col :span="6">
              <el-form-item>
                <el-input v-model="account.inn" placeholder="ИНН" />
              </el-form-item>  
            </el-col>
            <el-col :span="8">
              <el-form-item>
                <el-input v-model="account.passport_il.who_take" placeholder="Кем выдан" /> 
              </el-form-item>  
            </el-col>
          </el-row>
          <el-row style="margin-top:1em;">
            <el-col :span="4" :offset="4" style="padding-left:1.6em;">
              <el-upload
                action="#"
                v-model:file-list="account.passport_il.uploadFiles"
                class="upload-block"
                :limit="1"
                :auto-upload="false"
              >
                <el-button type="primary">Загрузить скан. паспорта</el-button>
                <template #tip>
                  <div class="el-upload__tip">
                    pdf файл размером не более 20 мб.
                  </div>
                </template>
              </el-upload>
            </el-col>
          </el-row>
          <el-row style="margin-top:1em;">
            <el-col :span="4"  :offset="16">
              <el-button type="info" @click="selectFIOFromDB(index)" style="width:98%;">Выбрать из базы</el-button>
            </el-col>
            <el-col :span="4">
              <el-button  class="mt-2" type="danger" @click="removeFIO(account)" :disabled="index === 0 ? true : false">Удалить запись Должник {{ index }}</el-button>
            </el-col>
          </el-row>     
        </el-col>
      </el-row>
      <el-row style="margin-top:1em;">
        <el-col :span="4" :offset="20">
          <el-button type="success" @click="addAccount">Добавить Физ. лицо</el-button>
        </el-col>  
      </el-row>  
    </el-form>
    <template>
      <el-dialog
        v-model="searchFIOVisible"
        width="40%"
        title="Inner Dialog"
        append-to-body
      >
        <el-input v-model="fioSearchinput" placeholder="Поиск по фамилии или имени или отчеству" clearable /> 
        <el-table
          :data="filterFIOData"
          highlight-current-row
          style="width: 100%"
          @current-change="handleFIOChange"
          height="450"
        >
          <el-table-column type="index" width="50" />
          <el-table-column property="surname" label="Фамилия" width="240" />
          <el-table-column property="name" label="Имя" width="200" />
          <el-table-column property="second_name" label="Отчество" />
        </el-table>
        <div style="margin-top: 20px">
          <el-button @click="setСhoise">Выбрать</el-button>
          <el-button @click="searchFIOVisible = false">Отмена</el-button>
        </div>
      </el-dialog>
    </template>       
        <template #footer>
        <span class="dialog-footer">
            <el-button @click="dialogVisible = false">Отмена</el-button>
            <el-button type="primary" @click.prevent="submitForm(ruleFormRef)">
            Сохранить
            </el-button>
        </span>
        </template>
  </el-dialog>
</template>

<script>
import { debt_il_get_all_accounts_il_list, debt_il_create_list_with_accounts_data } from '../../http/http-common'
import { reactive, defineComponent, toRef, toRaw } from 'vue'
import { dataType } from 'element-plus/es/components/table-v2/src/common'

export default defineComponent ({
  expose: ['dialogVisible'],
  setup() {
    const ruleForm = reactive({
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
        debt_sum_il: '',
        start_exec_pross_date: '',
        end_exec_pross_date: '',
        period:[],
        accounts_il: [
          {
            uuid: '',
            account_number: '',
            name: '',
            second_name: '',
            surname: '',
            inn: '',
            passport_il: {
              id: 1,
              seria: '',
              number: '',
              who_take: '',
              when_take: '',
              squad_code: '',
              birth_date: '',
              birth_place: '',
              scan: '',
              uploadFiles: [],
            } 
          }
        ],
      })

    const rules = reactive({
        street: [
            { required: true, message: 'Пожалуйста выберите улицу', trigger: 'blur' },
            //{ min: 3, max: 5, message: 'Length should be 3 to 5', trigger: 'blur' },
          ],
        home: [
            {
              required: true,
              message: 'Пожалуйста укажите номер дома',
              trigger: 'change',
            },
          ],
        appartment: [
            {
              required: true,
              message: 'Пожалуйста укажите номер квартиры',
              trigger: 'change',
            },
          ],
        one_or_parts: [
            {
              required: true,
              message: 'Пожалуйста выберите долю владения имуществом',
              trigger: 'change',
            },
          ],
        property_self: [
            {
              required: true,
              message: 'Пожалуйста выберите тип имущества',
              trigger: 'change',
            },
          ],
        il_number: [
            {
              required: true,
              message: 'Пожалуйста укажите номер исполнительного листа',
              trigger: 'change',
            },
          ],
        il_date: [
            {
              type: 'date',
              required: true,
              message: 'Пожалуйста укажите дату исполнительного листа',
              trigger: 'change',
            },
          ],
        period: [
            {
              type: 'array',
              required: false,
              message: 'Пожалуйста укажите период исполнительного производства',
              trigger: 'change',
            },
        ],
        gov_tax: [
            {
              required: true,
              message: 'Пожалуйста укажите гос. пошлину',
              trigger: 'change',
            },
        ],
        debt_sum_il: [
            {
              required: true,
              message: 'Пожалуйста укажите сумму задолженности',
              trigger: 'change',
            },
        ],
        accounts_il: [
          {
            type: 'array',
            required: true,
            defaultField: { 
              
            },
          },
        ],   
    })
    
    const ruleFormRef = toRef(ruleForm)

    return {
      ruleFormRef,ruleForm, rules
    }  
  },
  data() {
    return {
      dialogVisible: false,
      formSize: 'default',
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
      searchFIOVisible: false,
      accIndex: 0,
      currentFIO: null,
      fioData:[],
      fioSearchinput: '',
    }
  },
  methods:{
    async submitForm (formEl){
      console.log(formEl)
      await formEl.validate((valid, fields) => {
        if (valid) {
          //console.log('submit!', this.ruleForm)
          let data = toRaw(this.ruleForm)
          let formData = new FormData()     
          Object.keys(data).forEach(key =>{
            if (key === 'accounts_il') {
              data[key].forEach((account, index) => {
                if (account.passport_il.uploadFiles.length !=0) {
                  //mutliple append in key @files@ create list file objects
                  formData.append('files', account.passport_il.uploadFiles[0].raw,  account.passport_il.uploadFiles[0].name)
                  account.passport_il.uploadFiles = account.passport_il.uploadFiles[0].name
                }
                formData.append('accounts_il', JSON.stringify(account))
              })
            }
            formData.append(key, data[key])
          })
          console.log('-------->', data)
          console.log('-------->', formData.values)
          let result = debt_il_create_list_with_accounts_data(formData)
          console.log(result)
        } else {
          console.log('error submit!', fields)
          //console.log('-<<<<', this.ruleForm)
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
      this.ruleForm.accounts_il.push({
        account_number: '',
        name: '',
        second_name: '',
        surname: '',
        inn: '',
        passport_il: {
          serial: "74 05",
          number: "111111",
          who_take: "ОВД администрации города Трехгорного Челябинской области",
          when_take: "2022-11-02T10:56:04.116Z",
          squad_code: "740-000",
          birth_date: "2022-11-02T10:56:04.116Z",
          birth_place: "г Златоуст-36 Челябинской области",
          scan: "string",
          uploadFiles: [],
        }  
      })
    },
    async selectFIOFromDB (index) {
      this.searchFIOVisible = true
      this.accIndex = index
      if (this.fioData.length === 0) {
        this.fioData = await debt_il_get_all_accounts_il_list()
      }
    },
    handleFIOChange (val) {
      this.currentFIO = val
    },
    setСhoise () {
      if (!this.currentFIO.passport_il) {
        this.currentFIO.passport_il = {
          id: this.accIndex,
          seria: "",
          number: "",
          who_take: "",
          when_take: "",
          squad_code: "",
          birth_date: "",
          birth_place: "",
          scan: ""
        }
      }
      this.ruleForm.accounts_il[this.accIndex] = this.currentFIO
      console.log(this.currentFIO)
      this.accIndex = 0
      this.currentFIO = null,
      this.searchFIOVisible = false
    },
  },
  computed: {
    filterFIOData () {
      let filteredData = this.fioData.filter((data) => {
        if (this.fioSearchinput) {  
          if ((data.surname + ' ' + data.name + ' - ' + data.second_name).toLowerCase().includes(this.fioSearchinput.toLowerCase()))
            return data
        }   
      })

      if (filteredData.length) {
        return filteredData
      }else{
        return this.fioData
      }
    }      
  }
})
</script>

<style>
.el-form-item__label {
  word-break: break-word;
}
</style>

<style scoped>
.upload-block {
  display: inline;
}
.el-upload__tip {
  display: inline;
}
.acc-datapicker >>> .acc-datepicker_calendar {
  width: 100%;
}
</style>
