<template>
    <div>
    <el-row>
        <el-col :span="24">
            <el-divider content-position="left"><h2>Газовые счетчики</h2></el-divider>
        </el-col>
    </el-row>
    <el-row :gutter="12" v-for="(row, index) in gasRows" :key="index">
        <el-col :span="6" v-for="(item, innerindex) in row" :key="item.id" >
        <el-card shadow="always" > Always </el-card>
        </el-col>
    </el-row>
    </div> 
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
    setup() {
    },
    data () {
        return {

        }
    },
    props: {
        gasCounters: Array,
    },
    methods: {
        
    },
    computed : {
        gasRows () {
        const rows = []
        this.gasCounters.forEach((item, index) => {
            const row = Math. floor (index / 4) // 4 represents four rows, which can be changed at will
            if (!rows[row]) {
            rows[row] = []
            }
            rows[row].push(item)
        })
        return rows
        }
    }
})
</script>

<style scoped>

</style>