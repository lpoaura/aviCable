// /composables/useMyFetch.ts

export const useApi : typeof useHttp = (request, opts?) => {
  const config = useRuntimeConfig()
  console.log('useApi', config.public)
  return useHttp(request, { baseURL: config.public.baseURL, ...opts })
}

console.log("useApi",useApi)
