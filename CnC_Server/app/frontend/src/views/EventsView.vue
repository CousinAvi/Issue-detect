<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-12 mt-5">
        <h1>Ивенты в системе</h1>
        <input class="form-control form-control-lg mt-4" type="text" placeholder="Введите адрес или домен" v-model.lazy="query">
        <table class="table mt-5">
          <thead>
          <tr>
            <th scope="col text-center">Организация</th>
            <th scope="col text-center">Сервис</th>
            <th scope="col text-center">Причина</th>
            <th scope="col text-center">Комментарий</th>
          </tr>
          </thead>
          <tbody>
          <template v-for="event in events">
            <tr>
              <td>{{ event.company }}</td>
              <td>{{ event.service }}</td>
              <td>{{ event.reason }}</td>
              <td>{{ event.comment }}</td>
            </tr>
          </template>
          </tbody>
        </table>


      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref, watch} from "vue";
import axios from "axios";

const query = ref("")
const events = ref([])

const updateList = () => {
  axios.get(`/api/v1/get_ml_events?query=${query.value}`).then((data) => {
    events.value = data.data
  })
}

updateList()

watch(() => query.value, () => {
  updateList()
})

</script>

<style scoped>

</style>