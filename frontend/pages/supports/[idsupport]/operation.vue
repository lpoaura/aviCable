<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="support ? false : true" mode="point" /></template>
    <form-operation />
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
