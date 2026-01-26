import '@mdi/font/css/materialdesignicons.css'
// import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { VFileUpload } from 'vuetify/labs/VFileUpload'
import { VDateInput } from 'vuetify/labs/VDateInput'
import DateFnsAdapter from '@date-io/date-fns'
import {enUS} from 'date-fns/locale/en-US'
import {fr} from 'date-fns/locale/fr'
import {es} from 'date-fns/locale/es'
import {it} from 'date-fns/locale/it'

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
        fr: fr,
        es: es,
        it: it,
      },
    },
  })
  app.vueApp.use(vuetify)
})
