import { defineStore } from 'pinia'
import { jwtDecode, type JwtPayload } from 'jwt-decode'
import dayjs from 'dayjs'
import type { UserSimple, SignUpFormData, Credentials, Tokens } from '~/types/user'
import type { UseFetchOptions } from '#app'
import { useRouter } from 'vue-router';

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
type RequestData = Record<string, any> | FormData;


export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null as string | null | JwtPayload,
        isAuthenticated: false,
        authTokens: null as Tokens | null,
        userInfo: null as UserSimple | null
    }),
    actions: {
        async register(formData: SignUpFormData) {
            const config = useRuntimeConfig()

            try {
                const response = await fetch(`${config.public.baseURL}/api/v1/user/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData),
                })
                const data = await response.json()

                if (response.status !== 201) {
                    // Handle validation errors specifically
                    if (typeof data === 'object' && data !== null) {
                        const errors = Object.values(data)
                        if (errors.length > 0 && errors[0].length > 0) {
                            // Extract the first error message from the first property with an error
                            throw new Error(errors[0][0])
                        }
                    }

                    // Fallback error message if the structure wasn't as expected
                    throw new Error('Registration failed due to an unexpected error.')
                }

                return data // On success, return the response data
            } catch (error) {
                return {
                    error: error.message || 'An error occurred during registration.',
                }
            }
        },
        async login(credentials: Credentials): Promise<void> {
            console.log('login')
            const config = useRuntimeConfig()
            console.log('config.public', config.public)
            try {
                //const config = useRuntimeConfig()
                const response = await $fetch<Promise<Tokens>>(`${config.public.baseURL}/api/v1/auth/jwt/create/`, {
                    method: 'POST',
                    body: JSON.stringify(credentials),
                })

                const authTokens = response
                const user = jwtDecode(authTokens.access)

                this.user = user as JwtPayload
                this.isAuthenticated = true
                this.authTokens = authTokens

                localStorage.setItem('authTokens', JSON.stringify(authTokens))

                await this.fetchUser()
            } catch (error) {
                console.error('Login error:', error)
                throw error
            }
        },
        checkAuth() {
            this.authTokens = JSON.parse(localStorage.getItem('authTokens'))
            if (this.authTokens) {
                this.isAuthenticated = true
                this.user = jwtDecode(this.authTokens.access)
                // if (!this.userInfo) {
                //     this.userInfo = JSON.parse(localStorage.getItem('userInfo', JSON.stringify(userInfo)))
                // }
            }
        },
        async fetchUser(): Promise<UserSimple | null> {
            try {
                const { data } = await this.authedGet('/api/v1/auth/users/me/');
                this.userInfo = data  as UserSimple;

                localStorage.setItem('userInfo', JSON.stringify(this.userInfo));
                return this.userInfo;
            } catch (error) {
                console.error('Fetch user error:', error);
                throw error;
            }
        },
         async authedRequest<T>(
            url: string,
            originalConfig: UseFetchOptions<any, any> = {}
        ): Promise<T> {
            const config = { ...originalConfig };
            const router = useRouter();
            const envConfig = useRuntimeConfig();

            const accessToken = await this.retrieveValidToken();
            if (!accessToken) {
                router.push('/account/login');
                return Promise.reject('No auth token found') as any; // Adjust as needed
            }

            config.headers = {
                ...config.headers,
                Authorization: `JWT ${accessToken}`,
            };

            try {
                return await useFetch(`${envConfig.public.baseURL}/${url}`, config) as T;
            } catch (error) {
                console.error('Failed to make authenticated request:', error);
                return Promise.reject(error) as any; // Adjust as needed
            }
        },
        async makeRequest(method: M, url: string, data: RequestData = {}, config = {} as UseFetchOptions<unknown, unknown>): Promise<T> {
            const requestConfig = { ...config, method };
            
            if (data) {
                requestConfig.body = data;
            }
            
            return await this.authedRequest<T>(url, requestConfig);

            config.method = method
            if (data && Object.keys(data).length > 0) {
                config.data = data
            }
            return await this.authedRequest(url, config)
        },
        async authedPost(url: string, data: RequestData = {}, config = {}) {
            return this.makeRequest('POST', url, data, config)
        },
        async authedPut(url: string, data: RequestData = {}, config = {}) {
            return this.makeRequest('PUT', url, data, config)
        },
        async authedPatch(url:string, data: RequestData = {}, config = {}) {
            return this.makeRequest('PATCH', url, data, config)
        },
        async authedGet(url:string, config = {}) {
            return this.makeRequest('GET', url, null, config)
        },
        async authedDelete(url, config = {}) {
            return this.makeRequest('DELETE', url, null, config)
        },
        async retrieveValidToken() {
            this.authTokens = JSON.parse(localStorage.getItem('authTokens'))
            if (!this.authTokens) {
                return null
            }

            const user = jwtDecode(this.authTokens.access)
            // Set isExpired to true if token expires in less than a minute from now
            const isExpired = dayjs.unix(user.exp).diff(dayjs(), 'minute') < 1

            if (isExpired) {
                try {
                    const newTokens = await this.refreshToken()
                    if (newTokens) {
                        localStorage.setItem('authTokens', JSON.stringify(newTokens))
                        this.authTokens = newTokens
                        this.user = jwtDecode(newTokens.access)

                        return newTokens.access
                    }
                } catch (err) {
                    console.error('Error refreshing token', err)
                    return null
                }
            }

            return this.authTokens.access
        },
        async refreshToken() {
            const rToken = this.authTokens?.refresh
            if (!rToken) {
                console.error('No refresh token available')
                return null
            }

            try {
                const envConfig = useRuntimeConfig()
                const { data, error } = await useFetch(
                    `${envConfig.public.baseURL}/api/v1/auth/jwt/refresh`,
                    {
                        method: 'POST',
                        body: JSON.stringify({ refresh: rToken }),
                    },
                )
                console.error('<refreshToken> error ', error)
                return data
            } catch (error) {
                console.error('Failed to refresh token:', error)
                this.logout()
                return null
            }
        },
        logout() {
            this.user = null
            this.isAuthenticated = false
            this.userInfo = null
            localStorage.removeItem('authTokens')
        },
    },
})