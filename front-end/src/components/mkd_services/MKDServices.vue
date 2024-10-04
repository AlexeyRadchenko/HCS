<template>
    <div class="mkd-services-wrapper-conteiner">
        <el-container >
            <el-header>
                <el-row>
                    <el-col :span="8"><div class="service-title"><h1>{{ serviceTitle }}</h1></div></el-col>  
                    <el-col :span="12"><div></div></el-col>
                    <el-col :span="4"></el-col>
                </el-row>  
            </el-header>
            <el-main>
                <h1>Сервисы МКД {{ message }}</h1>
            </el-main>
        </el-container>
    </div>
  </template>
  
  <script setup>
  // Импортируйте необходимые функции, если нужно
  import { ref, reactive, computed, onMounted } from 'vue';
  
  // Создайте реактивные переменные
  const message = ref('Привет, Vue 3!');
  const serviceTitle = ref('Оказанные услуги (работы по МКД)')
  
  // Логика для компонента
  const count = ref(0);
  const increment = () => {
    count.value++;
  };
  
  onMounted(() => {
    console.log('Компонент был смонтирован!');
  });
  </script>
  
  <style scoped>
  .mkd-services-wrapper-conteiner {
    border: 1px solid #eee;
    border-radius: 10px;
    /*padding-top: 0.8em;*/
    /*background-color: burlywood;*/
    margin: 1em 2em;
  }
  .service-title {
    padding-top: 0.8em;
    color: black;
  }

  .debt-sub-table {
    margin-left: 4em;
  }
  </style>
  