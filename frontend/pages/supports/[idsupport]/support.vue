<template>
  <NuxtLayout name="view">
    <template #map><map-search :edit-mode="true" mode="point" /></template>
    <form-support :support="support" />
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

watch(support, (_val)=> {
  console.log('VAL', _val)
  console.log('support', support)
})

const getData = async () =>{
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
