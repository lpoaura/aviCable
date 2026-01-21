<template>
    <v-sheet width="100%" max-width="600" class="mx-auto">

        <v-form ref="signUpForm" v-model="formValid">
            <v-card class="mx-auto pa-12 pb-8" elevation="0" rounded="lg">
                <h1><v-icon>mdi-account-plus</v-icon> {{ $t('auth.createAccount') }}</h1>
                <div class="text-subtitle-1 text-medium-emphasis">{{ $t('auth.username') }}</div>
                <v-text-field v-model="formValue.username" density="compact" :placeholder="$t('auth.username')"
                    prepend-inner-icon="mdi-account-outline" variant="outlined" :rules="required" autofocus />

                <div class="text-subtitle-1 text-medium-emphasis">{{ $t('auth.firstName') }}</div>
                <v-text-field v-model="formValue.first_name" density="compact" :placeholder="$t('auth.firstName')"
                    prepend-inner-icon="mdi-account-outline" variant="outlined" :rules="required" />

                <div class="text-subtitle-1 text-medium-emphasis">{{ $t('auth.lastName') }}</div>
                <v-text-field v-model="formValue.last_name" density="compact" :placeholder="$t('auth.lastName')"
                    prepend-inner-icon="mdi-account-outline" variant="outlined" :rules="required" />

                <div class="text-subtitle-1 text-medium-emphasis">{{ $t('auth.email') }}</div>
                <v-text-field v-model="formValue.email" density="compact" :placeholder="$t('auth.email')"
                    prepend-inner-icon="mdi-account-outline" variant="outlined" :rules="required" />

                <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                    {{ $t('auth.password') }}
                </div>
                <v-text-field v-model="formValue.password" :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="visible ? 'text' : 'password'" density="compact" :placeholder="$t('auth.password')"
                    prepend-inner-icon="mdi-lock-outline" variant="outlined" :rules="passwordRules"
                    @click:append-inner="visible = !visible" />
                <v-progress-linear v-if="pwdStrength" v-model="pwdStrength.value" :color="pwdStrength.color" />

                <div class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between">
                    {{ $t('auth.confirmPassword') }}
                </div>
                <v-text-field v-model="confirmPassword" :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                    :type="visible ? 'text' : 'password'" density="compact" :placeholder="$t('auth.confirmPassword')"
                    prepend-inner-icon="mdi-lock-outline" variant="outlined" :rules="confirmPasswordRules" />


                <div class="text-subtitle-1 text-medium-emphasis">{{ $t('auth.areasOfIntervention') }}</div>
                <v-autocomplete v-model="formValue.areas" chips :items="areas" item-title="label" item-value="id"
                    :rules="listRequired" hide-selected :label="$t('auth.areasOfIntervention')" multiple deletable-chips
                    variant="outlined" density="compact" clearable required />

                <v-btn block class="mb-8" color="blue" size="large" variant="flat" :loading="loading"
                    :disabled="!formValid" @click="signUp()">
                    {{ $t('login.sign-up') }}
                </v-btn>
            </v-card>
        </v-form>
    </v-sheet>
</template>

<script setup type="ts">
import zxcvbn from 'zxcvbn';


const { t } = useI18n()
const router = useRouter()

const signUpForm = ref()
const confirmPassword = ref(null)
const formValid = ref(false)
const loading = ref(false)
const formValue = reactive({
    username: null,
    password: null,
    first_name: null,
    last_name: null,
    email: null,
    phone: null,
    organisms: null,
    areas: null
})
const required = reactive([v => !!v || t('valid.required')])
const listRequired = reactive([v => {
    return !!(v?.length) || t('valid.required')
}])
const passwordRules = reactive([
    (value) => !!value || t('auth.enterPassword'),
    (value) => (value && value.length >= 12) || t('auth.passwordMinLength'),
    (value) => zxcvbn(value).score >= 3 || t('auth.passwordStrengthRequired'),
])
const confirmPasswordRules = reactive([
    (value) => !!value || t('confirmPassword'),
    (value) =>
        value === formValue.password || t('auth.confirmPasswordNotMatch'),
])

const visible = ref(false)

const nomenclaturesStore = useNomenclaturesStore()
const notificationStore = useNotificationStore()

const { areas } = storeToRefs(nomenclaturesStore)

const pwdStrength = computed(() => {
    if (formValue.password) {
        const result = zxcvbn(formValue.password);

        switch (result.score) {
            case 4:
                return {
                    color: "light-blue",
                    value: 100
                };
            case 3:
                return {
                    color: "light-green",
                    value: 75
                };
            case 2:
                return {
                    color: "yellow",
                    value: 50
                };
            case 1:
                return {
                    color: "orange",
                    value: 25
                };
            default:
                return {
                    color: "red",
                    value: 0
                };
        }
    }
    return {
        color: "red",
        value: 0
    }
})

const signUp = async () => {
    console.log('proceed signUp', formValue)
    const { valid } = signUpForm.value.validate()
    if (valid) {
        const { data, error } = await useApi('/api/v1/user/', { method: 'post', body: formValue })
        if (error.value) {
            console.error(error.value.data)
            console.debug(data.value)
            custom_content =
                notificationStore.setInfo({
                    type: 'error',
                    msg: `${error.value}
            
            `
                })
        } else {
            router.push('/')
            notificationStore.setInfo({
                type: 'success',
                msg: `User ${data.value.username} successfully created, an email have been sent to administrators to valid your registration`
            })
        }
    }

}
</script>
