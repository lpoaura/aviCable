<template>
    <v-sheet width="100%" max-width="600" class="mx-auto text-center">
        <h1>{{ $t("auth.checkEmail") }}</h1>
        <div><v-icon :color="checkResp?.type" size="50">{{ icon }}</v-icon></div>
        <div>{{ checkResp?.msg }}</div>

    </v-sheet>
</template>

<script lang="ts" setup>
import type { NotificationInfo } from '~/types/notifications'

const notificationStore = useNotificationStore()

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const token = computed(() => route.query.token)

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

const checkStatus = ref(null)
const checkResp = ref<NotificationInfo | null>(null)

const checkEmail = async () => {
    const { data, error } = await authStore.authedGet<NotificationInfo>(`/api/v1/user/verify_email/${token.value}/`)
    checkResp.value = data.value
    if (checkResp.value) {
        notificationStore.setInfo(checkResp.value)
        checkStatus.value = checkResp.value.type
    }
    else {
        notificationStore.setInfo({
            type: 'error',
            msg: error.value?.message
        })
    }
    await sleep(5000)
    router.push('/')
}

onMounted(() => {
    checkEmail()
})

</script>
