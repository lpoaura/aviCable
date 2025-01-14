import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { VFileUpload } from 'vuetify/labs/VFileUpload'
import {VDateInput} from 'vuetify/labs/VDateInput'

export default defineNuxtPlugin((app) => {
  const vuetify = createVuetify({
    ssr: true,
    theme: {
      defaultTheme: 'light'
    },
    components: {
      VFileUpload,
      VDateInput,
    },
  })
  app.vueApp.use(vuetify)
})
