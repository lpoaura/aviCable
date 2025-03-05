export const useApi : typeof useHttp = (request, opts?) => {
  const config = useRuntimeConfig()
  return useHttp(request, { baseURL: config.public.baseURL, ...opts })
}
