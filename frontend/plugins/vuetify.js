import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { VFileUpload } from 'vuetify/labs/VFileUpload'
import { VDateInput } from 'vuetify/labs/VDateInput'
import DateFnsAdapter from '@date-io/date-fns'
import enUS from 'date-fns/locale/en-US'
import frFR from 'date-fns/locale/fr'
import esES from 'date-fns/locale/es'
import itIT from 'date-fns/locale/it'

export default defineNuxtPlugin((app) => {
  const vuetify = createVuetify({
    locale: {
      locale: 'fr'
    },
    ssr: true,
    theme: {
      defaultTheme: 'light'
    },
    components: {
      VFileUpload,
      VDateInput,
    },
    date: {
      adapter: DateFnsAdapter,
      locale: {
        en: enUS,
        fr: frFR,
        es: esES,
        it: itIT,
      },
    },
  })
  app.vueApp.use(vuetify)
})
