// import { useAuthStore } from '@/store/authStore'

// type ApiOptions = Omit<RequestInit, 'method' | 'body'>

// export function useApi() {
//   const auth = useAuthStore()
//   const config = useRuntimeConfig()

//   async function request<T>(
//     method: string,
//     url: string,
//     body?: any,
//     options: ApiOptions = {}
//   ): Promise<T> {
//     return auth.authedFetch<T>(url, {
//       method,
//       body,
//       headers: {
//         'Content-Type': 'application/json',
//         ...(options.headers || {}),
//       },
//     })
//   }

//   return {
//     get: <T>(url: string, options?: ApiOptions) =>
//       request<T>('GET', url, undefined, options),

//     post: <T>(url: string, body?: any, options?: ApiOptions) =>
//       request<T>('POST', url, body, options),

//     put: <T>(url: string, body?: any, options?: ApiOptions) =>
//       request<T>('PUT', url, body, options),

//     patch: <T>(url: string, body?: any, options?: ApiOptions) =>
//       request<T>('PATCH', url, body, options),

//     delete: <T>(url: string, options?: ApiOptions) =>
//       request<T>('DELETE', url, undefined, options),
//   }
// }

// export function usePublicApi() {
//   const config = useRuntimeConfig()

//   return {
//     post<T>(url: string, body?: any) {
//       return $fetch<T>(`${config.public.baseURL}${url}`, {
//         method: 'POST',
//         body,
//       })
//     },
//   }
// }
