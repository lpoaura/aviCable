<template>
  <v-card elevation="0" class="fill-height">
    <v-form ref="form" v-model="formValid">
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12" class="text-left">
              <strong> {{ $t('forms.generalInfrastructure') }}</strong>
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
    </v-form>
  </v-card>

</template>

<script lang="ts" setup>
import { storeToRefs } from 'pinia';
import * as errorCodes from '~/static/errorConfig.json'
import type { NotificationInfo } from '~/types/notifications'
import type { CablesFeature } from '~/types/cables';

const emit = defineEmits();

const coordinatesStore = useCoordinatesStore()
const nomenclaturesStore = useNomenclaturesStore()
const cablesStore = useCablesStore()
const notificationStore = useNotificationStore()

const { t } = useI18n()

interface Props {
  infrastructure?: Ref<CablesFeature>,
  infrastructureType: string
}

const { infrastructure, infrastructureType } = defineProps<Props>()

// data
const form = ref(null) // used to get form ref from "<v-form ref="form">"
const formValid = ref(true)

const route = useRoute()
const router = useRouter()

// Adding operations

const { newGeoJSONObject } = storeToRefs(coordinatesStore)
const { ownerItems } = storeToRefs(nomenclaturesStore)
const infrastructureId = computed(() => route.params.id)

const infrastructureData = reactive({
  geom: {},
  owner_id: null,
});

// Watch for changes in the infrastructure prop
watch(
  () => infrastructure,
  (newInfrastructure) => {
    console.log('wATCHER INFRA', newInfrastructure, infrastructure)
    if (newInfrastructure?.value) {
      infrastructureData.geom = newInfrastructure.value.geometry;
      infrastructureData.owner_id = newInfrastructure.value.properties?.owner?.id;
    }
  },
  { immediate: true } // This will also run the watcher immediately with the current value
);



const rules = reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  requiredOrNotValid: (v: string | number) => v === 0 || !!v || t('valid.required_or_not_valid'),
  latRange: (v: number) => (v >= 40 && v <= 52) || `${t('valid.range')}40 : 52`,
  lngRange: (v: number) => (v >= -20 && v <= 20) || `${t('valid.range')}-20 : 20`,
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})

const moveToNextStep = async () => {
  const formInfrastructure = await createNewInfrastructure()
  if (formInfrastructure) {
    if (!infrastructureId.value) {
      emit('nextStep');
    } else {
      router.push(`/infrastructures/${infrastructureId.value}`)
    }
  } 
};


const createNewInfrastructure = async () => {
  try {
    infrastructureData.geom = newGeoJSONObject.value?.geometry
    const url = infrastructureId.value ? `/api/v1/cables/${infrastructureType.toLowerCase()}s/${infrastructureId.value}/` : `/api/v1/cables/${infrastructureType.toLowerCase()}s/`
    const method = infrastructureId.value ? 'put': 'post'
    const { data, error } = await useApi<CablesFeature>(url, { method, body: infrastructureData })
    cablesStore.setFormInfrastructureId(data.value?.properties?.id)
    if (error.value) {
      notificationStore.setInfo({
        type: 'error',
        msg: error
      })
    } else {
      notificationStore.setInfo({
        type: 'success',
        msg: 'Infrastructure créée'
      })
    }
    return data?.value
  } catch (_err) {
    console.error(_err)
    const error: NotificationInfo = {
      type: 'error',
      msg: t(`error.${errorCodes.create_point.msg}`)
    }
    notificationStore.setInfo(error)
  }
}

</script>
