<template>
    <v-container class="fill-height pa-0" fluid>
        <v-row v-if="!mobile" class="fill-height">
            <v-col cols="6" class="pr-0 pt-0 pb-0">
                <slot name="map">
                    <map-search :edit-mode="false" />
                </slot>
            </v-col>
            <v-col cols="6" class="pa-0 fill-height">
                <slot></slot>
            </v-col>
        </v-row>

        <template v-if="mobile">
            <v-card class="fill-height" width="100%">
              <!--   <v-tabs v-model="tab" grow density='compact'>
                    <v-tab value="map"> {{ $t('app.map') }} </v-tab>
                    <v-tab value="data"> {{ $t('app.data') }} </v-tab>
                    <v-tab value="map"><v-icon>mdi-map</v-icon></v-tab>
                    <v-tab value="data"><v-icon>mdi-format-list-bulleted</v-icon></v-tab>
                </v-tabs>

                <v-card-text class="fill-height pa-0">
                    <v-window v-model="tab" class="fill-height">
                        <v-window-item value="map" class="fill-height">
                            <slot name="map">
                                <map-search :edit-mode="false" />
                            </slot>
                        </v-window-item>
                        <v-window-item value="data">
                            <slot />
                        </v-window-item>
                    </v-window>
                </v-card-text>-->
                <v-card-text class="fill-height pa-0">
                    <map-search :edit-mode="false" />
                </v-card-text>
            </v-card>
        </template>
    </v-container>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'
const tab=ref('map')
const {mobile} = useDisplay()

onMounted (() => {
    // TODO fix reactive value
    // mdAndUp.value=true
})
</script>
