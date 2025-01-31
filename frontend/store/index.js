// DO NOT REMOVE THIS FILE even if empty !!!
// Creating this file activate the store of the application
import { createPinia } from 'pinia'
const pinia = createPinia()

import { useErrorsStore } from './errorStore';

const errorStore = useErrorsStore(pinia)

export { pinia, errorStore }
