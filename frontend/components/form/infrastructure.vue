<template>
  <v-card elevation="0" class="fill-height">
    <v-form ref="form" v-model="formValid">
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" class="text-left">
              <strong> {{ $t('forms.generalInfrastructure') }}</strong> {{ infrastructureType.toLowerCase() }}
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" lg="12">
              <v-select v-model="infrastructureData.owner_id" :items="ownerItems" item-title="label" item-value="id"
                :rules="[rules.required]" :label="$t('support.network')" variant="solo" density="compact" required />
            </v-col>
          </v-row>
        </v-container>

      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="success" :disabled="!formValid" variant="flat" prepend-icon="mdi-content-save-all"
          @click="moveToNextStep">Sauvegarder</v-btn>
      </v-card-actions>
      {{ infrastructureData }}
    </v-form>
  </v-card>

</template>

<script lang="ts" setup>
import { storeToRefs } from 'pinia';
import * as errorCodes from '~/static/errorConfig.json'
import type { ErrorInfo } from '~/store/errorStore';

const emit = defineEmits();

const coordinatesStore = useCoordinatesStore()
const nomenclaturesStore = useNomenclaturesStore()
const cablesStore = useCablesStore()
const errorStore = useErrorsStore()

const { t } = useI18n()

interface Props {
  infrastructure?: object,
  infrastructureType: string
}
const upc = ref(null)
// data
const form = ref(null) // used to get form ref from "<v-form ref="form">"
const formValid = ref(true)

const { infrastructure, infrastructureType } = defineProps<Props>()

// Adding operations

const { newGeoJSONObject } = storeToRefs(coordinatesStore)
const { ownerItems } = storeToRefs(nomenclaturesStore)

const infrastructureData = reactive({
  geom: null,
  owner_id: infrastructure ? infrastructure.owner_id : null,
})


const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  requiredOrNotValid: (v: string | number) => v === 0 || !!v || t('valid.required_or_not_valid'),
  latRange: (v: number) => (v >= 40 && v <= 52) || `${t('valid.range')}40 : 52`,
  lngRange: (v: number) => (v >= -20 && v <= 20) || `${t('valid.range')}-20 : 20`,
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})

const moveToNextStep = async () => {
  const infrastructure = await createNewInfrastructure()
  if (infrastructure) {
    emit('nextStep');
  }
};


const createNewInfrastructure = async () => {
  try {
    infrastructureData.geom = newGeoJSONObject.value?.geometry
    const { data: infrastructure } = await useHttp(`/api/v1/cables/${infrastructureType.toLowerCase()}s/`, { method: 'post', body: infrastructureData })
    cablesStore.setFormInfrastructureId(infrastructure.value.properties.id)
    return infrastructure?.value
  } catch (_err) {
    console.error(_err)
    const error: ErrorInfo = {
      code: errorCodes['create_point']['code'],
      msg: t(`error.${errorCodes.create_point.msg}`)
    }
    errorStore.setError(error)
  }
}
</script>
