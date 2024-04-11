<template>
    <v-container>
        <v-row>
            <v-col cols="12" class="text-left">
                <h2>{{ $t('display.operation') }}</h2>
            </v-col>
        </v-row>
        <v-row>
            <input type="hidden" :value="operation.id" />
            <v-col cols="12" md="6">
                <v-menu>
                    <template v-slot:activator="{ props }">
                        <v-text-field v-model="operation.date" :label="$t('forms.datecreate')" persistent-hint
                            :rules="[rules.required]" inner-prepend-icon="mdi-calendar" variant="solo" density="compact"
                            v-bind="props" required />
                    </template>
                    <v-date-picker v-model="operation.date" no-title show-adjacent-months color="primary"></v-date-picker>
                </v-menu>
            </v-col>
            <v-col cols="12" md="6">

                <v-select v-model="operation.operation_type" :items="getNomenclatureByType('operation_type')"
                    item-title="label" item-value="id" :rules="[rules.required]" :label="$t('support.condition')"
                    variant="solo" density="compact" required></v-select>
            </v-col>
            <v-col cols="12">
                <v-list lines="one">
                    <template v-for="(find, index) in operation.equipements" :key="index">
                        <v-list-item :prepend="index">
                            <template v-slot:prepend>
                                <v-avatar size="x-small" color="grey-lighten-1">
                                    {{ index+1}}
                                </v-avatar>
                            </template>
                            <template v-slot:append>
                                <v-avatar size="x-small" color="red-lighten-1"
                                    @click="operation.equipements.splice(index, 1)">
                                    <v-icon>mdi-delete</v-icon>
                                </v-avatar>
                            </template>
                            <v-row class="pa-1">
                                <v-col cols="12" md="4">
                                    <v-select v-model="find.type" :items="getNomenclatureByType('equipment_type')"
                                        item-title="label" item-value="id" :rules="[rules.required]" required
                                        label="Type d'équipement" variant="solo" density="compact"></v-select>
                                </v-col>
                                <v-col cols="12" md="4">
                                    <v-text-field type="number" density="compact" v-model="find.count" variant="solo"
                                        :rules="[rules.required]" label="Nombre" required />
                                </v-col>
                                <v-col cols="12" md="4">
                                    <v-text-field v-model="find.reference" density="compact" variant="solo"
                                        label="Référence" />
                                </v-col>
                                <v-col cols="12">
                                    <v-text-field v-model="find.comment" density="compact" variant="solo"
                                        label="Commentaire" />
                                </v-col>
                            </v-row>

                        </v-list-item>
                        <v-divider></v-divider>
                    </template>
                </v-list>
                <v-btn block color="info" @click="addEquipement">
                    <v-icon>mdi-plus</v-icon>New Equipement
                </v-btn>
            </v-col>
            <v-divider></v-divider>
            <v-col cols="12">
                <v-textarea v-model="operation.remark" clearable clear-icon="mdi-close-circle" :label="$t('app.remark')"
                    :rules="[rules.textLength]" rows="2" counter="300" variant="solo" density="compact"></v-textarea>
            </v-col>
        </v-row>
        <code><pre>{{ operation }}</pre></code>
    </v-container>
</template>

<script lang="ts" setup>
import { storeToRefs } from 'pinia'

interface Equipement {
    id?: number;
    type: string;
    count: number;
    reference: string;
    comment: string;
}

interface Operation {
    id?: number;
    date: string;
    operation_type: number;
    equipements: Equipement[];
}

const valid:boolean=ref<boolean>(false)

const { t } = useI18n()
const nomenclatureStore = useNomenclaturesStore()
const { getNomenclatureByType } = storeToRefs(nomenclatureStore)
const operation : Operation = reactive<Operation>({
    date: new Date(),
    operation_type: null,
    equipements: [{} as Equipement],
})

const emits = defineEmits(['operation'])

emits('operation', operation)

const rules =  reactive({
  required: (v: string | number) => !!v || t('valid.required'),
  requiredOrNotValid: (v: string | number) => v === 0 || !!v || t('valid.required_or_not_valid'),
  latRange: (v: number) => (v >= 40 && v <= 52) || `${t('valid.range')}40 : 52`,
  lngRange: (v: number) => (v >= -20 && v <= 20) || `${t('valid.range')}-20 : 20`,
  textLength: (v: string) => (v || '').length <= 300 || `${t('valid.length')}: 300`,
})

const addEquipement = () => {
    operation.equipements.push({} as Equipement);
}
</script>