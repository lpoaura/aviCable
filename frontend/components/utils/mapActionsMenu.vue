<template>
  <div class="d-flex align-end float-right ma-5">
    <v-menu transition="fade-transition">
      <template v-if="!$parent.editMode" #activator="{ props }">
        <v-btn id="speedDial" dark color="primary" icon="mdi-plus" v-bind="props" class="float-right" />
      </template>
      <v-btn fab dark class="ma-1" icon="mdi-shape-polygon-plus" size="small" color="orange" />
      <v-btn fab dark class="ma-1" icon="mdi-transmission-tower" size="small" to="/infrastructures/new?type=point"
        color="green" />
      <v-btn fab dark class="ma-1" icon="mdi-cable-data" size="small" to="/infrastructures/new?type=line"
        color="indigo" />
      <v-btn fab dark class="ma-1" icon="mdi-coffin" size="small" to="/mortality/new" color="red" />
    </v-menu>
  </div>
</template>

<script setup>


</script>
<style>
#speedDial {
  z-index: 10000;
}
</style>
