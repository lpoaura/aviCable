<template>
  <NuxtLayout name="view">
    <template #map>
      <map-search :edit-mode="true" :mode="infrastructureType" />
    </template>
    <v-layout full-height>
      <v-app-bar density="compact" color="blue-grey-lighten-5">
        <v-app-bar-title>
          Edition d'une infrastructure
        </v-app-bar-title>
        <v-app-bar-nav-icon>
          <v-btn density="compact" icon="mdi-close" @click="$router.push(`/infrastructures/${infrastructureId}`)" />
        </v-app-bar-nav-icon>
      </v-app-bar>
      <v-main scrollable>
        <v-container>
          <!-- <div>
            <pre>{{ infrastructure }}</pre>
          </div> -->
          <form-infrastructure :infrastructure="infrastructure" :infrastructure-type="infrastructureType" />
        </v-container>
      </v-main>
    </v-layout>

  </NuxtLayout>
</template>



<script setup>
definePageMeta({
  auth: true,
});

const authStore = useAuthStore()
const coordinatesStore = useCoordinatesStore()
const route = useRoute()

const infrastructure = ref({})
const infrastructureId = computed(() => route.params.id)
const infrastructureType = computed(() => route.query.type?.toLowerCase())

const getData = async () => {
  console.debug('getData route.params.id', infrastructureId.value);
  if (infrastructureId.value) {
    try {
      const { data } = await authStore.authedGet(`/api/v1/cables/infrastructures/${infrastructureId.value}`);
      infrastructure.value = data; // Assign the fetched data to the infrastructure ref
      coordinatesStore.setSelectedFeature(data); // Assuming data is the correct structure
    } catch (error) {
      console.error('Error fetching infrastructure data:', error);
      // Handle error (e.g., show a notification or set an error state)
    }
  }
};

onMounted(async () => {
  await getData()
  console.debug('infrastructure mounted', infrastructure)
})

</script>
