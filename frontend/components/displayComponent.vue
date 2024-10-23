<template>
  <v-layout full-height>
    <v-main>
      <v-tabs v-model="tab" bg-color="light-blue-darken-4" grow>
        <v-tab value="#infra">
          <v-badge color="info" :content="countInfstr || '-'" floating>{{
            $t('display.infrastructures') }}</v-badge>
        </v-tab>
        <v-tab value="#mortality" bg-color="red">
          <v-badge color="error" :content="countMortality || '-'" floating>{{ $t('display.mortalityCases') }}
          </v-badge>
        </v-tab>
      </v-tabs>

      <v-window v-model="tab" class="fill-height">
        <v-window-item value="#infra" class="fill-height">
          <data-display-infrastructure />
        </v-window-item>
        <v-window-item value="#mortality" class="fill-height">
          <data-display-mortality />
        </v-window-item>
      </v-window>
    </v-main>
  </v-layout>
</template>
<script setup>
import { storeToRefs } from 'pinia';
import { ref } from 'vue'
const tab = ref('#infra')

const route = useRoute()
const router = useRouter()
const cableStore = useCablesStore()
const mortalityStore = useMortalityStore()

const { countInfstr } = storeToRefs(cableStore)
const { countMortality } = storeToRefs(mortalityStore)

watch(tab, (value) => {
  router.push(`${route.path}${value}`)
})

onMounted(() => {
  router.push(`${route.path}${tab.value}`)
})
</script>
