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

const getInfo = async () => {
    try {
        const data = await api.get<UserSimple>(`/api/v1/user/activate/${token.value}/`)
        user.value = data
    } catch (error) {
        if (error && error instanceof Error) {
            notificationStore.setInfo({
                type: 'error',
                msg: error.message
            })
        }
        else {
            notificationStore.setInfo({
                type: 'error',
                msg: `${error}`
            })
        }
    }
}

const activateUser = async () => {
    try {
        const data = await api.patch<NotificationInfo>(`/api/v1/user/activate/${token.value}/`)
        notificationStore.setInfo(data)
        checkStatus.value = data.type
    } catch (error) {
        if (error && error instanceof Error) {
            notificationStore.setInfo({
                type: 'error',
                msg: error.message
            })
        }
        else {
            notificationStore.setInfo({
                type: 'error',
                msg: `${error}`
            })
        }
        checkStatus.value = 'error'
    }
    await sleep(2000)
    router.push("/")
}

onMounted(() => getInfo())

</script>
