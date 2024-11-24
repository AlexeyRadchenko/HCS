<template>
<div class="limiter">
    <div class="container-login100 container-bg">
        <div class="wrap-login100">
            <form class="login100-form validate-form" v-on:submit.prevent="onSubmit">
                <span class="login100-form-logo">
                    <font-awesome-icon :icon="['fa', 'house-user']" size="1x" />
                </span>

                <span class="login100-form-title p-b-34 p-t-27">
                    Личный Кабинет
                </span>

                <div class="wrap-input100 validate-input" data-validate = "Enter username">
                    <input class="input100" type="text" name="username" placeholder="Лицевой счет" v-model="username">
                    <span class="focus-input100"><font-awesome-icon :icon="['fa', 'user']" size="2x" /></span>   
                </div>

                <div class="wrap-input100 validate-input street-wrap" data-validate="Улица">
                    <select class="input100 input-sel" v-model="selected_street" >
                        <option value="" disabled hidden>Улица</option>
                        <option v-for="street in streets" :key="street.label">{{ street.value }}</option>
                        
                    </select>
                    <span class="focus-input100"><font-awesome-icon :icon="['fa', 'road']" size="2x" /></span>
                </div>

                <div class="wrap-input100 validate-input" data-validate = "Введите номер дома">
                    <input class="input100" type="text" name="house" placeholder="Номер дома" v-model="house">
                    <span class="focus-input100"><font-awesome-icon :icon="['fa', 'building']" size="2x" /></span>   
                </div>

                <div class="wrap-input100 validate-input" data-validate = "Введите номер квартиры">
                    <input class="input100" type="text" name="appartment" placeholder="Квартира" v-model="appartment">
                    <span class="focus-input100"><font-awesome-icon :icon="['fa', 'list-ol']" size="2x" /></span>   
                </div>

                <div class="container-login100-form-btn">
                    <button class="login100-form-btn" v-on:click="loading">
                        Вход
                    </button>
                </div>
                <!--<div class="text-center p-t-60">
                    <a class="txt1" href="#">
                        Forgot Password?
                    </a>
                </div>-->
            </form>
        </div>
    </div>
</div> 
</template>

<style scoped>
@import "../assets/clients_authorisation/css/main.module.css";
@import "../assets/clients_authorisation/css/utils.module.css";

.container-bg {
    background-image: url('../assets/clients_authorisation/images/bg-01.jpg')
}

.input-sel {
    /* margin-left: 5.2em;*/
    width: 77%;
    background-size: 12px;
    /*padding-left: 2em;*/
    font-size: 1.45rem;
    border: none;
    outline:0px;
    background-color: #944CF6;
}
.input-sel option {
    margin-left: 1.2em;
}

.street-wrap {
    padding-left: 5.4rem;
}

select {
    text-align: center;
    text-align-last: center;
    -moz-text-align-last: center;
}
</style>

<script>
import { accountLogin } from '../http/account-http-common';
import { useAccountAuthStore } from '../storage/accountAuthService';
import { ElLoading } from 'element-plus';

export default {
    setup() {
        const authStore = useAccountAuthStore()
        return { authStore }
    },
    data() {
      return {
        selected_street: '',
        username: '',
        password: 'secret',
	    loading: null,
        streets:[
            {
                value: '50 лет Победы',
                label: '50 лет Победы',
            },
            {
                value: '60 лет Октября',
                label: '60 лет Октября',
            },
            {
                value: 'Володина',
                label: 'Володина',
            },
            {
                value: 'Калинина',
                label: 'Калинина',
            },
            {
                value: 'Карла Маркса',
                label: 'Карла Маркса',
            },
            {
                value: 'Кирова',
                label: 'Кирова',
            },
            {
                value: 'Космонавтов',
                label: 'Космонавтов',
            },
            {
                value: 'Ленина',
                label: 'Ленина',
            },
            {
                value: 'Маршала Жукова',
                label: 'Маршала Жукова',
            },
            {
                value: 'Мира',
                label: 'Мира',
            },
            {
                value: 'Островского',
                label: 'Островского',
            },
            {
                value: 'Потапова',
                label: 'Потапова',
            },
            {
                value: 'Советская',
                label: 'Советская',
            },
            {
                value: 'Строителей',
                label: 'Строителей',
            },
        ],
        house: '',
        appartment: '',
      }
    },
    methods: {
        onSubmit () {
            var userFormData = new FormData();
            userFormData.append('username', this.username)
            userFormData.append('password', this.password)
            userFormData.append('street', this.selected_street)
            userFormData.append('house', this.house)
            userFormData.append('appartment', this.appartment)
            const loading = ElLoading.service({
                    lock: true,
                    text: 'Загрузка',
                    background: "rgba(0, 0, 0, 0.85)"
                })
            accountLogin(this.authStore, userFormData, loading, this.$router)
        }
    }
}
</script>

