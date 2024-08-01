<template>
  <v-layout full-height>
    <v-app-bar density="compact" color="blue-grey-lighten-5">
      <v-app-bar-title>
        <v-icon icon="mdi-coffin" color="red"></v-icon>#{{data.id}}
        <strong>{{ data.properties.species.vernacular_name }}</strong>
      </v-app-bar-title>

      <v-spacer />
      <v-app-bar-nav-icon>
        <v-btn density="compact" icon="mdi-close" @click="$router.push('/search#mortality')" />
      </v-app-bar-nav-icon>
    </v-app-bar>
    <v-main scrollable>
      <v-container>
        <p>
          <span class="font-weight-bold">Espèce&nbsp;:</span>
          {{ data.properties.nb_death ? data.properties.nb_death: 'x' }} {{data.properties.species.vernacular_name }}
          (<i>{{data.properties.species.scientific_name }} </i>)
        </p>
        <p>
          <span class="font-weight-bold">Date&nbsp;:</span>
          {{data.properties.date }}
        </p>
        <p>
          <span class="font-weight-bold">Observateur&nbsp;:</span>
          {{data.properties.author }}
        </p>
        <p>
          <span class="font-weight-bold">Cause de mortalité&nbsp;:</span>
          {{data.properties.death_cause.label }}
        </p>
        <p>
          <span class="font-weight-bold">Infrastructure associée&nbsp;:</span>
          {{data.properties.infrstr ? data.properties.infrstr : '-' }}
        </p>
        <p>
          <span class="font-weight-bold">Source de la donnée&nbsp;:</span>
          {{data.properties.data_source ? data.properties.data_source : '-' }}
        </p>
        <!-- <pre>{{data}}</pre> -->
      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
// const router = useRouter()
const {data} = defineProps(['data'])
console.debug('props.data' , data)
</script>
