// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ["@vite-pwa/nuxt", [
    "@pinia/nuxt",
    {
      autoImports: ["defineStore", "acceptHMRUpdate"],
    },
  ], "@invictus.codes/nuxt-vuetify", "@nuxtjs/i18n", "@nuxt/eslint"],
  ssr: false,
  app: {
    head: {
      title: 'aviCable',
    }
  },
  pwa: {
    registerType: 'autoUpdate',
    manifest: {
      name: 'Avifaune & cables aériens',
      short_name: 'aviCable',
      theme_color: '#0277bd',
      icons: [
        {
          src: 'pwa-192x192.png',
          sizes: '192x192',
          type: 'image/png',
        },
        {
          src: 'pwa-512x512.png',
          sizes: '512x512',
          type: 'image/png',
        },
        {
          src: 'pwa-512x512.png',
          sizes: '512x512',
          type: 'image/png',
          purpose: 'any maskable',
        },
      ],
    },
    workbox: {
      navigateFallback: "/",
      globPatterns: ["**/*.{js,css,html,json,ico,png,svg}"],
    },
    client: {
      installPrompt: true,
      // you don't need to include this: only for testing purposes
      // if enabling periodic sync for update use 1 hour or so (periodicSyncForUpdates: 3600)
      periodicSyncForUpdates: 20,
    },
    devOptions: {
      enabled: true,
      suppressWarnings: true,
      navigateFallbackAllowlist: [/^\/$/],
      type: 'module',
    },
  },

  vuetify: {
    /* vuetify options */
    vuetifyOptions: {
      // @TODO: list all vuetify options
      date: {
        adapter: 'vuetify' // 'vuetify' | 'date-fns' | 'moment' | 'luxon' | 'dayjs' | 'js-joda' | 'date-fns-jalali' | 'jalaali' | 'hijri' | 'custom'
      }
    },
    moduleOptions: {
      /* nuxt-vuetify module options */
      treeshaking: true,
      useIconCDN: true,
      /* vite-plugin-vuetify options */
      styles: true,
      autoImport: true,
    },
  },
  css: [
    "vuetify/lib/styles/main.css",
    "@mdi/font/css/materialdesignicons.min.css",
    "leaflet/dist/leaflet.css",
    "@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css",
    'leaflet.locatecontrol/dist/L.Control.Locate.min.css',
    "leaflet-geosearch/assets/css/leaflet.css"
  ],
  build: {
    transpile: ["vuetify", "leaflet-geoman"],
  },
  imports: {
    // Auto-import pinia stores defined in `~/stores`
    dirs: ["store"],
  },
  i18n: {
    locales: [
      { code: "en", language: "en-US", file: "en.json" },
      { code: "fr", language: "fr-FR", file: "fr.json" },
    ],

    defaultLocale: "fr",
    langDir: "locales",
  },
  runtimeConfig: {
    public: {
      baseURL: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },
  http: {},
  compatibilityDate: "2024-07-15",
});