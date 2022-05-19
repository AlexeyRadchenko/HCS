<template>
    <el-container class="account-wrapper-conteiner">
        <el-tabs
            v-model="activeName"
            type="border-card"
            class="account-tabs"
            :stretch="true"
        >
            <el-tab-pane label="Информация" name="info">User</el-tab-pane>
            <el-tab-pane label="Счетчики" name="counters"><AccountCounters v-loading="loading" :dataLoading="loading" /></el-tab-pane>
            <el-tab-pane label="Квитанции" name="payments">Role</el-tab-pane>
            <el-tab-pane label="Task" name="fourth">Task</el-tab-pane>
        </el-tabs>
    </el-container>
    
</template>

<script>
import { defineComponent } from 'vue'
import AccountCounters from './AccountCounters.vue'
import { useAccountAuthStore } from '../../storage/accountAuthService'
import { get_account_data_by_acc } from '../../http/account-http-common'

export default defineComponent ({
    components: {
        AccountCounters
    },
    setup() {
        const accAuthStore = useAccountAuthStore()
        return { accAuthStore }
    },
    data () {
        return {
            activeName: 'info',
            accountData: null,
            loading: true
        }
    },
    methods: {
       
    },
    computed: {
    },
    async created () {
       var data  = await get_account_data_by_acc (this.accAuthStore.getUser.account)
       this.accAuthStore.setAccountData(data)
       this.loading = false
    },
})
</script>

<style>
.account-wrapper-conteiner {
  border: 1px solid #eee;
  border-radius: 10px;
  /*padding-top: 0.8em;*/
  /*background-color: burlywood;*/
  margin: 1em 2em;
  height:100%;
}
.account-tabs {
    width: 100%;
}
</style>