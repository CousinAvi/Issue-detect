<template>
  <div class="container mt-5">
    <!--    <div class="row justify-content-center">-->
    <!--        <div class="mt-5 text-center text-dark bg-light">-->
    <!--            <h2>Проверьте свой сайт</h2>-->
    <!--        </div>-->
    <!--    </div>-->
    <input class="form-control form-control-lg mt-4" type="text" placeholder="Введите адрес или домен" v-model.lazy="query">
    <table class="table mt-5">
      <thead>
      <tr>
        <th scope="col text-center">Организация</th>
        <th scope="col text-center">Ресурс</th>
        <th scope="col text-center">Причина</th>
        <th scope="col text-center">Время</th>
      </tr>
      </thead>
      <tbody>
      <template v-for="event in events">
        <tr>
          <td>{{event.bank_name}}</td>
          <td>{{event.url}}</td>
          <td>{{event.log}}</td>
          <td>{{event.timestamp}}</td>
        </tr>
      </template>
      </tbody>
    </table>

  </div>
</template>

<script lang="ts" setup>
import {ref, watch} from "vue";
import axios from "axios";

const events = ref([])
const query = ref("")

const getEvents = () => {
  axios.get(`/api/v1/get_bot_logs?query=${query.value}`).then((data)=>{
    events.value = data.data
  })
}

getEvents()

watch(()=>query.value, (oldVakue, newValue) => {
  getEvents()
})


</script>
