<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="support ? false : true" mode="point" /></template>
    <v-layout full-height>
      <v-app-bar density="compact" color="blue-grey-lighten-5">
        <v-app-bar-title>
          Edition du diagnostic
        </v-app-bar-title>
      </v-app-bar>
      <v-main scrollable>
        <v-container>
          <form-point-diagnosis :diagnosis="diagnosis" :support="support" />
        </v-container>
      </v-main>
    </v-layout>
  </NuxtLayout>
</template>



<script setup>
import { defineAsyncComponent } from 'vue'

const FormPoint = defineAsyncComponent(() =>
  import('~/components/form/point.vue')
)

const cablesStore = useCablesStore()

definePageMeta({
  auth: true,
});
const route = useRoute()
const diagnosis = ref(null)
const support = ref(null)
const supportId = computed(() => route.params.idsupport)

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
  cablesStore.setFormSupportId(supportId.value)
})

</script>UT
