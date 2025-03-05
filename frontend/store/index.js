// DO NOT REMOVE THIS FILE even if empty !!!
// Creating this file activate the store of the application
import { createPinia } from 'pinia'
import { useNotificationStore } from './notificationStore';

const pinia = createPinia()

const notificationStore = useNotificationStore(pinia)

export { pinia, notificationStore }
