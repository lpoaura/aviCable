<template>
  <v-layout full-height>
    <v-main scrollable>
      <v-tabs v-model="tab" bg-color="light-blue-darken-4" grow>
        <v-tab value="#infra" bg-color="green"> {{ $t('display.infrastructures') }} </v-tab>
        <!-- <v-tab value="#support"> {{ $t('support.supports-eqmt') }} </v-tab>
        <v-tab value="#sensitivearea">
          {{ $t('display.sensitiveAreas') }}
        </v-tab> -->
        <v-tab value="#mortality" bg-color="red"> {{ $t('display.mortalityCases') }} </v-tab>
      </v-tabs>

      <v-window v-model="tab">
        <v-window-item value="#infra">
          <data-display-infrastructure />
        </v-window-item>
        <!-- <v-window-item value="#support">
          <data-equipment-display />
        </v-window-item>

        <v-window-item value="#sensitivearea">
          <data-sens-area-display />
        </v-window-item> -->
        <v-window-item value="#mortality">
          <data-display-mortality />
        </v-window-item>
      </v-window>
    </v-main>
  </v-layout>
</template>
<script setup>
import { ref } from 'vue'
const tab = ref('#infra')

const route = useRoute()
const router = useRouter()

watch(tab, (value) =>{
  router.push(`${route.path}${value}`)
})

onMounted(() => {
  router.push(`${route.path}${tab.value}`)
})
</script>

<style>
/* .v-tab {
  width: 100px;
  background-color: 'indigo';
} */
</style>
