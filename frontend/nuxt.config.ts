// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ["@vite-pwa/nuxt", "@nuxt-alt/auth", "@nuxt-alt/http", [
    "@pinia/nuxt",
    {
      autoImports: ["defineStore", "acceptHMRUpdate"],
    },
  ], "@invictus.codes/nuxt-vuetify", "@nuxtjs/i18n", "@nuxt/eslint"],

  ssr: false,

  pwa: {
    registerType: 'autoUpdate',
    manifest: {
      name: 'Cables & avifaune',
      short_name: 'ocb',
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

  // devtools: {
  //     // Enable devtools (default: true)
  //     enabled: true,
  //     // VS Code Server options
  //     vscode: {},
  //     // ...other options
  // },
  // routeRules: {
  //     '/api/v1/**': { cors: true, headers: { 'access-control-allow-methods': 'GET' }, proxy: 'http://localhost:8000' }
  // },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },

  http: {},

  auth: {
    // cookie: false,
    redirect: {
      login: "/account/login",
      logout: "/",
      callback: "/account/login",
      home: "/",
    },
    // globalMiddleware: true,
    strategies: {
      local: {
        scheme: "refresh",
        cookie: false,
        token: {
          property: "access", // property name of access token get from Back-end
          // global: true,
          // required: true,
          maxAge: 1800,
          type: "JWT",
        },
        refreshToken: {
          // it sends request automatically when the access token expires, and its expire time has set on the Back-end
          property: "refresh", // property name of refresh token get from Back-end
          data: "refresh", // data can be used to set the name of the property you want to send in the request.
          maxAge: 60 * 60 * 24 * 30,
        },
        user: {
          property: false,
          autoFetch: true,
        },
        endpoints: {
          login: {
            url: "/api/v1/auth/jwt/create/",
            method: "post",
          },
          refresh: { url: "/api/v1/auth/jwt/refresh", method: "post" },
          logout: false, //  there is no endpoint for logout in API. Just remove the token from localstorage
          user: {
            url: "/api/v1/auth/users/me/",
            method: "get",
            property: true,
          },
          reset: {
            url: "/api/v1/auth/reset_password/",
            method: "post",
          }
        },
      },
    },
  },

  compatibilityDate: "2024-07-15",
});
