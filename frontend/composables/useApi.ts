export const useApi : typeof useHttp = (request, opts?) => {
  const config = useRuntimeConfig()
  console.debug('<useApi ...opts>',opts, request)
  return useHttp(request, { baseURL: config.public.baseURL, ...opts })
}
