<template>
  <div class="container mt-3">
    <div class="row">
      <div class="col-12 mt-3">
        <h1>Найденная информация</h1>
        <h2>Ошибка 404</h2>
        <table class="table mt-3">
          <thead>
          <tr>
            <th scope="col text-center">Организация</th>
            <th scope="col text-center">Ресурс</th>
            <th scope="col text-center">Описание проблемы</th>
          </tr>
          </thead>
          <tbody>
          <template v-for="event in events404">
            <tr>
              <td>{{ event["Организация"] }}</td>
              <td>{{ event["ресурс"] }}</td>
              <td>{{ event["issue"] }}</td>
            </tr>
          </template>
          </tbody>
        </table>
        <h2>Ошибка 500</h2>
        <table class="table mt-3">
          <thead>
          <tr>
            <th scope="col text-center">Организация</th>
            <th scope="col text-center">Ресурс</th>
            <th scope="col text-center">Описание проблемы</th>
          </tr>
          </thead>
          <tbody>
          <template v-for="event in events500">
            <tr>
              <td>{{ event["Организация"] }}</td>
              <td>{{ event["ресурс"] }}</td>
              <td>{{ event["issue"] }}</td>
            </tr>
          </template>
          </tbody>
        </table>
        <h2>Ошибка 502</h2>
        <table class="table mt-3">
          <thead>
          <tr>
            <th scope="col text-center">Организация</th>
            <th scope="col text-center">Ресурс</th>
            <th scope="col text-center">Описание проблемы</th>
          </tr>
          </thead>
          <tbody>
          <template v-for="event in events502">
            <tr>
              <td>{{ event["Организация"] }}</td>
              <td>{{ event["ресурс"] }}</td>
              <td>{{ event["issue"] }}</td>
            </tr>
          </template>
          </tbody>
        </table>
        <h2>Ошибка 503</h2>
        <table class="table mt-3">
          <thead>
          <tr>
            <th scope="col text-center">Организация</th>
            <th scope="col text-center">Ресурс</th>
            <th scope="col text-center">Описание проблемы</th>
          </tr>
          </thead>
          <tbody>
          <template v-for="event in events503">
            <tr>
              <td>{{ event["Организация"] }}</td>
              <td>{{ event["ресурс"] }}</td>
              <td>{{ event["issue"] }}</td>
            </tr>
          </template>
          </tbody>
        </table>
        <h2>Отсутсвие записи в DNS</h2>
        <table class="table mt-3">
          <thead>
          <tr>
            <th scope="col text-center">Организация</th>
            <th scope="col text-center">Ресурс</th>
            <th scope="col text-center">Описание проблемы</th>
          </tr>
          </thead>
          <tbody>
          <template v-for="event in eventsARecord">
            <tr>
              <td>{{ event["Организация"] }}</td>
              <td>{{ event["ресурс"] }}</td>
              <td>{{ event["issue"] }}</td>
            </tr>
          </template>
          </tbody>
        </table>
        <h2>Некорректные настройки или отсутсвие шифрования</h2>
        <table class="table mt-3">
          <thead>
          <tr>
            <th scope="col text-center">Организация</th>
            <th scope="col text-center">Ресурс</th>
            <th scope="col text-center">Описание проблемы</th>
          </tr>
          </thead>
          <tbody>
          <template v-for="event in eventsCI">
            <tr>
              <td>{{ event["Организация"] }}</td>
              <td>{{ event["ресурс"] }}</td>
              <td>{{ event["issue"] }}</td>
            </tr>
          </template>
          </tbody>
        </table>
        <h2>Истекший сертификат шифрования</h2>
        <table class="table mt-3">
          <thead>
          <tr>
            <th scope="col text-center">Организация</th>
            <th scope="col text-center">Ресурс</th>
            <th scope="col text-center">Описание проблемы</th>
          </tr>
          </thead>
          <tbody>
          <template v-for="event in eventsExpired">
            <tr>
              <td>{{ event["Организация"] }}</td>
              <td>{{ event["ресурс"] }}</td>
              <td>{{ event["issue"] }}</td>
            </tr>
          </template>
          </tbody>
        </table>
        <h2>Самоподписанный сертификат шифрования</h2>
        <table class="table mt-3">
          <thead>
          <tr>
            <th scope="col text-center">Организация</th>
            <th scope="col text-center">Ресурс</th>
            <th scope="col text-center">Описание проблемы</th>
          </tr>
          </thead>
          <tbody>
          <template v-for="event in eventsSelfSigned">
            <tr>
              <td>{{ event["Организация"] }}</td>
              <td>{{ event["ресурс"] }}</td>
              <td>{{ event["issue"] }}</td>
            </tr>
          </template>
          </tbody>
        </table>
        <h2>Сервис не отвечает</h2>
        <table class="table mt-3">
          <thead>
          <tr>
            <th scope="col text-center">Организация</th>
            <th scope="col text-center">Ресурс</th>
            <th scope="col text-center">Описание проблемы</th>
          </tr>
          </thead>
          <tbody>
          <template v-for="event in eventsTimeOut">
            <tr>
              <td>{{ event["Организация"] }}</td>
              <td>{{ event["ресурс"] }}</td>
              <td>{{ event["issue"] }}</td>
            </tr>
          </template>
          </tbody>
        </table>
        <h2>Слишком много перенаправлений</h2>
        <table class="table mt-3">
          <thead>
          <tr>
            <th scope="col text-center">Организация</th>
            <th scope="col text-center">Ресурс</th>
            <th scope="col text-center">Описание проблемы</th>
          </tr>
          </thead>
          <tbody>
          <template v-for="event in eventsTooManyRedirects">
            <tr>
              <td>{{ event["Организация"] }}</td>
              <td>{{ event["ресурс"] }}</td>
              <td>{{ event["issue"] }}</td>
            </tr>
          </template>
          </tbody>
        </table>


      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref} from "vue";
import axios from "axios";

const events404 = ref([])
const eventsARecord = ref([])
const events500 = ref([])
const events502 = ref([])
const events503 = ref([])
const eventsCI = ref([])
const eventsExpired = ref([])
const eventsSelfSigned = ref([])
const eventsTimeOut = ref([])
const eventsTooManyRedirects = ref([])

axios.get("/404.json").then((data) => {
  events404.value = data.data["issues"]
})

axios.get("/500.json").then((data) => {
  events500.value = data.data["issues"]
})

axios.get("/502.json").then((data) => {
  events502.value = data.data["issues"]
})

axios.get("/503.json").then((data) => {
  events503.value = data.data["issues"]
})

axios.get("/cipherIssues.json").then((data) => {
  eventsCI.value = data.data["issues"]
})

axios.get("/expired.json").then((data) => {
  eventsExpired.value = data.data["issues"]
})

axios.get("/selfSigned.json").then((data) => {
  eventsSelfSigned.value = data.data["issues"]
})

axios.get("/timeOut.json").then((data) => {
  eventsTimeOut.value = data.data["issues"]
})

axios.get("/tooManyRedirects.json").then((data) => {
  eventsTooManyRedirects.value = data.data["issues"]
})

axios.get("/A-record.json").then((data) => {
  eventsARecord.value = data.data["issues"]
})
</script>

<style scoped>
h2 {
  margin-top: 80px;
}
</style>