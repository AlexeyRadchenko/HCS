<template>
<div class="limiter">
    <div class="container-login100 container-bg">
        <div class="wrap-login100">
            <form class="login100-form validate-form">
                <span class="login100-form-logo">
                    <font-awesome-icon :icon="['fa', 'house-user']" size="1x" />
                </span>

                <span class="login100-form-title p-b-34 p-t-27">
                    Личный Кабинет
                </span>

                <div class="wrap-input100 validate-input" data-validate = "Enter username">
                    <input class="input100" type="text" name="username" placeholder="Лицевой счет">
                    <span class="focus-input100"><font-awesome-icon :icon="['fa', 'user']" size="2x" /></span>   
                </div>

                <div class="wrap-input100 validate-input" data-validate="Улица">
                    <select class="input100 input-sel">
                        <option selected disabled hidden>Улица</option>
                        <option>Вававава</option>
                        <option>Тарваыораыа</option>
                    </select>
                    <span class="focus-input100"><font-awesome-icon :icon="['fa', 'road']" size="2x" /></span>
                </div>

                <div class="wrap-input100 validate-input" data-validate = "Enter username">
                    <input class="input100" type="text" name="username" placeholder="Номер дома">
                    <span class="focus-input100"><font-awesome-icon :icon="['fa', 'list-ol']" size="2x" /></span>   
                </div>

                <div class="wrap-input100 validate-input" data-validate = "Enter username">
                    <input class="input100" type="text" name="username" placeholder="Квартира">
                    <span class="focus-input100"><font-awesome-icon :icon="['fa', 'hashtag']" size="2x" /></span>   
                </div>

                <div class="container-login100-form-btn">
                    <button class="login100-form-btn">
                        Вход
                    </button>
                </div>

                <div class="text-center p-t-60">
                    <a class="txt1" href="#">
                        Forgot Password?
                    </a>
                </div>
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
    margin-left: 4.2em;
    width: 79%;
    background-size: 16px;
    padding-left: 2em;
    font-size: 20px;
}
.input-sel option {
    margin-left: 4.2em;
}
</style>

<script>

export default {
    setup() {
        
    },
    data() {
      return {
        value: '',
        options:[
            {
                value: 'Option1',
                label: 'Option1',
            },
            {
                value: 'Option2',
                label: 'Option2',
            },
            {
                value: 'Option3',
                label: 'Option3',
            },
            {
                value: 'Option4',
                label: 'Option4',
            },
            {
                value: 'Option5',
                label: 'Option5',
            },
            ]
      }
    }
}
</script>

