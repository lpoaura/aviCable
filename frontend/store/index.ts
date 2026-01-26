import { createPinia } from 'pinia'


const pinia = createPinia()

const notificationStore = useNotificationStore(pinia)
const authStore = useAuthStore(pinia)

export { pinia, notificationStore, authStore }
