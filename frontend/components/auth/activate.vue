<template>
    <v-sheet width="100%" max-width="600" class="mx-auto text-center">
        <v-card class="mx-auto pa-12 pb-8" elevation="0" rounded="lg">
            <h1><v-icon :color="checkStatus" size="50">{{ icon }}</v-icon> {{ $t('auth.accountActivation') }}</h1>
            <div v-if="user">
                <p><code>{{ user?.username }}</code></p>
                <p>{{ user?.full_name }}</p>
                <p>{{ user?.email }}</p>
            </div>

            <div><v-btn :disabled="disabled" block @click="activateUser()" class="mt-5" color="success">{{
                $t('auth.activate') }}</v-btn>
            </div>
        </v-card>
    </v-sheet>
</template>

<script lang="ts" setup>
import type { UserSimple } from '~/types/user'
import type { NotificationInfo } from '~/types/notifications'

const notificationStore = useNotificationStore()


const route = useRoute()
const router = useRouter()
const token = computed(() => route.query.token)
const user = ref<UserSimple | null>(null)
const disabled = ref(false)

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

const icon = computed(() => {
    switch (checkStatus.value) {
        case 'error':
            return 'mdi-alert-circle';
        case 'info':
            return 'mdi-information-outline';
        case 'success':
            return 'mdi-check-circle';
        default:
            return 'mdi-help-circle-outline';
    }

})

const checkStatus = ref<string>()
const checkResp = ref<NotificationInfo | null>(null)

// const { data, error } = await useApi<UserSimple | NotificationInfo>(`/api/v1/user/activate/${token.value}/`)

// watch(() => data, async (newVal) => {
//     console.error('WATCH DATA', typeof newVal, newVal)
//     if (newVal) {
//         notificationStore.setInfo({
//             type: newVal.type,
//             msg: newVal.msg
//         })
//     }
// })

// watch(() => error, async (newVal) => {
//     console.error('WATCH ERROR', typeof newVal, newVal)
//     if (newVal) {
//         notificationStore.setInfo({
//             type: 'error',
//             msg: `${newVal}`
//         })
//     }
// })

const getInfo = async () => {
    const { data, error, status } = await useApi<UserSimple>(`/api/v1/user/activate/${token.value}/`)
    console.debug(data.value)
    user.value = data.value
    console.debug(error.value)
    console.debug('status', status.value)
    if (error.value) {
        console.debug('response', error.value.response)
        if (error.value.response?.status === 401) {
            notificationStore.setInfo({
                type: 'error',
                msg: `You must be logged in to activate an account`
            })
        }
        else {
            notificationStore.setInfo({
                type: 'error',
                msg: `An error occured: ${error.value}`
            })
        }
    }
}

const activateUser = async () => {
    console.debug('activate')
    const { data, error } = await useApi<NotificationInfo>(`/api/v1/user/activate/${token.value}/`, { method: 'PATCH' })
    if (error.value) {
        notificationStore.setInfo({
            type: 'error',
            msg: `Can't get data for user : ${error.value}`
        })
        checkStatus.value = 'error'
    }
    if (data.value) {
        notificationStore.setInfo(data.value)
        checkStatus.value = data.value.type
    }
    await sleep(2000)
    router.push("/")
}

onMounted(() => getInfo())

</script>
