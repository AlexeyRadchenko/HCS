<template>
  <el-dialog v-model="dialogVisible" title="Создать запись" width="80%" draggable>
    <el-form
      ref="ruleFormRef"
      :model="ruleForm"
      :rules="rules"
      label-width="120px"
      :size="formSize"
      status-icon
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="Адрес" required>
            <el-select v-model="ruleForm.street" class="m-2" placeholder="Улица" style="width:100%;" >
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>  
        </el-col>
        <el-col :span="6">
          <el-input v-model="ruleForm.home" />
        </el-col>
        <el-col :span="6">
          <el-input v-model="ruleForm.appartment" />
        </el-col>  
      </el-row>
      <el-form-item label="Activity zone" prop="region">
        <el-select v-model="ruleForm.region" placeholder="Activity zone">
          <el-option label="Zone one" value="shanghai" />
          <el-option label="Zone two" value="beijing" />
        </el-select>
      </el-form-item>
      <el-form-item label="Activity count" prop="count">
        <el-select-v2
          v-model="ruleForm.count"
          placeholder="Activity count"
          :options="options"
        />
      </el-form-item>
      <el-form-item label="Activity time" required>
        <el-col :span="11">
          <el-form-item prop="date1">
            <el-date-picker
              v-model="ruleForm.date1"
              type="date"
              label="Pick a date"
              placeholder="Pick a date"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
        <el-col class="text-center" :span="2">
          <span class="text-gray-500">-</span>
        </el-col>
        <el-col :span="11">
          <el-form-item prop="date2">
            <el-time-picker
              v-model="ruleForm.date2"
              label="Pick a time"
              placeholder="Pick a time"
              style="width: 100%"
            />
          </el-form-item>
        </el-col>
      </el-form-item>
      <el-form-item label="Instant delivery" prop="delivery">
        <el-switch v-model="ruleForm.delivery" />
      </el-form-item>
      <el-form-item label="Activity type" prop="type">
        <el-checkbox-group v-model="ruleForm.type">
          <el-checkbox label="Online activities" name="type" />
          <el-checkbox label="Promotion activities" name="type" />
          <el-checkbox label="Offline activities" name="type" />
          <el-checkbox label="Simple brand exposure" name="type" />
        </el-checkbox-group>
      </el-form-item>
      <el-form-item label="Resources" prop="resource">
        <el-radio-group v-model="ruleForm.resource">
          <el-radio label="Sponsorship" />
          <el-radio label="Venue" />
        </el-radio-group>
      </el-form-item>
      <el-form-item label="Activity form" prop="desc">
        <el-input v-model="ruleForm.desc" type="textarea" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm(ruleFormRef)"
          >Create</el-button
        >
        <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
      </el-form-item>
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
        region: '',
        count: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: '',
      },
      rules: {
        name: [
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
      options:[
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
      ]
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
  }
}
</script>

<style scoped>

</style>