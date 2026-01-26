import { useAuthStore } from '@/store/authStore'

type ApiOptions = Omit<RequestInit, 'method'>

export const api = {
  get<T>(url: string, options: ApiOptions = {}) {
    return request<T>('GET', url, options)
  },

  post<T>(url: string, body?: any, options: ApiOptions = {}) {
    return request<T>('POST', url, { ...options, body })
  },

  put<T>(url: string, body?: any, options: ApiOptions = {}) {
    return request<T>('PUT', url, { ...options, body })
  },

  patch<T>(url: string, body?: any, options: ApiOptions = {}) {
    return request<T>('PATCH', url, { ...options, body })
  },

  delete<T>(url: string, options: ApiOptions = {}) {
    return request<T>('DELETE', url, options)
  },
}

async function request<T>(
  method: string,
  url: string,
  options: ApiOptions
): Promise<T> {
  const auth = useAuthStore()

  return auth.authedFetch<T>(url, {
    method,
    ...options,
    body: options.body ? JSON.stringify(options.body) : undefined,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  })
}
