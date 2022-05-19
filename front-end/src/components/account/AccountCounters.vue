<template>
    <div>
        <WaterCounter :waterCounters="waterCounters" :account="accAuthStore.getUser.account" v-if="waterCounters.length"/>
        <GasCounter :gasCounters="gasCounters" v-if="gasCounters.length" />
    </div>    
</template>

<script>
import { defineComponent } from 'vue'
import { useAccountAuthStore } from '../../storage/accountAuthService'
import WaterCounter from './counters/waterCounter.vue'
import GasCounter from './counters/GasCounter.vue'

export default defineComponent({
    components: {
        WaterCounter,
        GasCounter
    },
    setup() {
        const accAuthStore = useAccountAuthStore()
        return { accAuthStore }
    },
    data () {
        return {
            
        }
    },
    props: {
        dataLoading: Boolean,
    },
    computed: {
        waterCounters () {
            if (!this.dataLoading) {
            return this.accAuthStore.getAccountData.water_counters
            }
            return []
        },
        gasCounters () {
            if (!this.dataLoading) {
            return this.accAuthStore.getAccountData.gas_counters
            }
            return []
        },
    }    
})
</script>

<style scoped>

</style>