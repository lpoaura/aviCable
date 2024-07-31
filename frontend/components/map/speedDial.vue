<template>
  <v-speed-dial class="fab mb-5" absolute bottom right direction="top" transition="slide - y - reverse - transition">
    <template v-if="!editMode" #activator>
      <v-btn color="primary darken-2" dark fab>
        <v-icon x-large> + </v-icon>
      </v-btn>
    </template>
    <v-btn fab dark small color="orange">
      <v-icon>mdi-shape-polygon-plus</v-icon>
    </v-btn>
    <v-btn fab dark small to="/infrastructures/new?type=point" color="green">
      <v-icon>mdi-transmission-tower</v-icon>
    </v-btn>
    <v-btn fab dark small to="/infrastructures/new?type=line" color="indigo">
      <v-icon>mdi-cable-data</v-icon>
    </v-btn>
    <v-btn fab dark small to="/mortality/new" color="red">
      <v-icon>mdi-coffin</v-icon>
    </v-btn>
  </v-speed-dial>
</template>
<style>
.fab {
  z-index: 10000;
}
</style>
