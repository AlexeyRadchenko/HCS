<template>
    <el-container
        class="user-status-header-container"
    >      
        <el-header class="user-status-header">
            <el-row>
                <el-col :span="8" class="nav-menu-column">
                    <el-dropdown                   
                    >
                        <div class="nav-manu-wrapper">  
                            <font-awesome-icon :icon="['fas', 'bars']" size="2x" />
                        </div>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item><router-link to="/services" exact>Все сервисы</router-link></el-dropdown-item>
                                <el-dropdown-item>Задолженность по и/л</el-dropdown-item>
                                <el-dropdown-item>Соглашения с должниками</el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </el-col>
                <el-col :span="8"><div class="grid-content bg-purple"></div></el-col>
                <el-col :span="8" class="user-column">
                    <el-dropdown>
                        <div class="prof-icon-wrapper">
                            <span class="username-style noselect">
                                <font-awesome-icon :icon="['fas', 'user-check']" size="1x" />
                                {{ authStore.getUser.login }}
                            </span>
                        </div>
                        <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item>Выход</el-dropdown-item>
                        </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </el-col>
            </el-row>
        </el-header>

    </el-container>
</template>

<style scoped>
.user-status-header-container {
    height: 50px;
    border: 1px solid #eee;
    border-radius: 10px;
    /*padding-top: 0.8em;*/
    background-color: burlywood;
    margin: 1em 2em;

}
.user-status-header {
    width: 100%;
}
.prof-icon-wrapper {
    margin-right: 8px;
}
.username-style {
    font-size: 1.3em;
    color:black;
    margin-top: 1.2em;
    
}
.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Old versions of Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Edge, Opera and Firefox */
}

.user-column {
    text-align: right;
    padding-top: 0.8em;
}
.nav-manu-wrapper {
    color:black;
}
.nav-menu-column {
    padding-top: 0.7em;
}
.custom-active {
    color:black;
    background-color: blue;
    text-decoration: none;
}
.exact-active {
    color:black;
    text-decoration: none;
}

</style>

<script>
import { defineComponent } from 'vue'
import { useAuthStore } from '../storage/auth';

export default defineComponent({
    setup() {
        const authStore = useAuthStore()

        return { authStore }
    },
    data () {
        return {

        }
    }
})
</script>
