<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="support ? false : true" mode="point" /></template>
    <v-layout full-height>
      <v-app-bar density="compact" color="blue-grey-lighten-5">
        <v-app-bar-title>
          Edition d'une opération
        </v-app-bar-title>
      </v-app-bar>
      <v-main scrollable>
        <v-container>
          <form-operation />
        </v-container>
      </v-main>
    </v-layout>

  </NuxtLayout>
</template>



<script setup>

const cablesStore = useCablesStore()

definePageMeta({
  auth: true,
});
const route = useRoute()
const diagnosis = ref(null)
const support = ref(null)
const supportId = computed(() => route.params.idsupport)

const modifyDiag = computed(() => route.query.modifyDiag === 'true' ? true : false)

onMounted(()=> {
  cablesStore.setFormSupportId(supportId.value)
})

</script>UT
