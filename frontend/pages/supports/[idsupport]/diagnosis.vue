<template>
  <v-container class="fill-height pa-0" fluid>
    <NuxtLayout name="view">
      <template #map><map-search :edit-mode="support ? false : true" mode="point" /></template>
      <form-point :diagnosis="diagnosis" :support="support" />
    </NuxtLayout>
  </v-container>
</template>



<script setup>
import { defineAsyncComponent } from 'vue'

const FormPoint = defineAsyncComponent(() =>
  import('~/components/form/point.vue')
)

definePageMeta({
  middleware: 'auth',
  layout: false
})
const route = useRoute()
const diagnosis = ref(null)
const support = ref(null)

const modifyDiag = computed(() => route.query.modifyDiag === 'true' ? true : false)

watch(support, (_val)=> {
  console.log('VAL', _val)
  console.log('support', support)
})

const getData = async () =>{
  if (route.query.id_diagnosis) {
    console.debug(`load Diag AdminPageComponentdata ${route.query.id_diagnosis}`)
   await useHttp(`/api/v1/cables/diagnosis/${route.query.id_diagnosis}`).then(res => diagnosis.value=res.data)
   console.debug('DIAG VALUES', diagnosis.value)
  }
  if (route.params.idsupport) {
    console.log('route.params.idsupport',route.params.idsupport)
    await useHttp(`/api/v1/cables/infrastructures/${route.params.idsupport}`).then(res=> {
      support.value=res.data
    })
  }
}

onMounted(()=> {
  getData()
})
</script>
