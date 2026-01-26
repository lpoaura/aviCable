import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'
import dayjs from 'dayjs'
import type { UserSimple, Credentials } from '~/types/user'

interface AuthTokens {
    access: string
    refresh: string
}

interface JwtPayload {
    user_id: number
    exp: number
    email?: string
}

interface AuthedFetchOptions extends RequestInit {
    _retry?: boolean
}

export const useAuthStore = defineStore('auth', {
    state: () => ({
        authTokens: null as AuthTokens | null,
        user: null as JwtPayload | null,
        userInfo: null as UserSimple | null,
        isAuthenticated: false,
    }),

    getters: {
        accessToken: (state) => state.authTokens?.access ?? null,
    },

    actions: {
        /* ----------------------------------------------------
         * Init / Hydration
         * -------------------------------------------------- */
        init() {
            if (process.server) return

            const stored = localStorage.getItem('authTokens')
            if (!stored) return

            this.authTokens = JSON.parse(stored)
            this.user = jwtDecode(this.authTokens.access)
            this.isAuthenticated = true

            this.fetchUserInfo().catch(() => {
                // Si erreur, ignore (ou logout selon besoin)
            })
        },

        /* ----------------------------------------------------
         * Auth
         * -------------------------------------------------- */
        async login(credentials: Credentials) {
            const config = useRuntimeConfig()

            const tokens = await $fetch<AuthTokens>(
                `${config.public.baseURL}/api/v1/auth/jwt/create/`,
                {
                    method: 'POST',
                    body: { ...credentials },
                }
            )

            this.setTokens(tokens)

            await this.fetchUserInfo()
        },

        logout() {
            this.authTokens = null
            this.user = null
            this.isAuthenticated = false
            this.userInfo = null

            if (process.client) {
                localStorage.removeItem('authTokens')
            }

            navigateTo('/account/login')
        },

        /* ----------------------------------------------------
         * Token handling
         * -------------------------------------------------- */
        setTokens(tokens: AuthTokens) {
            this.authTokens = tokens
            this.user = jwtDecode(tokens.access)
            this.isAuthenticated = true

            if (process.client) {
                localStorage.setItem('authTokens', JSON.stringify(tokens))
            }
        },
        async fetchUserInfo() {
            try {
                this.userInfo = await this.authedFetch<UserSimple>(
                    '/api/v1/auth/users/me/'
                )
            } catch (err) {
                console.error('Impossible de récupérer les infos utilisateur', err)
                this.userInfo = null
            }
        },
        async refreshToken(): Promise<string | null> {
            if (!this.authTokens?.refresh) return null

            const config = useRuntimeConfig()

            try {
                const data = await $fetch<{ access: string }>(
                    `${config.public.baseURL}/api/v1/auth/jwt/refresh/`,
                    {
                        method: 'POST',
                        body: { refresh: this.authTokens.refresh },
                    }
                )

                this.setTokens({
                    access: data.access,
                    refresh: this.authTokens.refresh,
                })

                return data.access
            } catch {
                this.logout()
                return null
            }
        },

        async getValidAccessToken(): Promise<string | null> {
            if (!this.authTokens) return null

            const payload = jwtDecode<JwtPayload>(this.authTokens.access)
            const isExpired = dayjs.unix(payload.exp).diff(dayjs(), 'second') < 30

            if (!isExpired) return this.authTokens.access

            return await this.refreshToken()
        },

        /* ----------------------------------------------------
         * Authenticated requests (à utiliser partout)
         * -------------------------------------------------- */
        async authedFetch<T>(
            url: string,
            options: AuthedFetchOptions = {}
        ): Promise<T> {
            const config = useRuntimeConfig()
            const token = await this.getValidAccessToken()

            if (!token) {
                this.logout()
                throw new Error('Not authenticated')
            }

            try {
                return await $fetch<T>(`${config.public.baseURL}${url}`, {
                    ...options,
                    headers: {
                        ...(options.headers || {}),
                        Authorization: `JWT ${token}`,
                    },
                })
            } catch (error: any) {
                const status = error?.response?.status

                /**
                 * 🔁 CAS RETRY
                 * - 401
                 * - pas déjà retentée
                 */
                if (status === 401 && !options._retry) {
                    const newToken = await this.refreshToken()

                    if (!newToken) {
                        this.logout()
                        throw error
                    }

                    // 🔁 rejoue la requête UNE fois
                    return this.authedFetch<T>(url, {
                        ...options,
                        _retry: true,
                        headers: {
                            ...(options.headers || {}),
                            Authorization: `JWT ${newToken}`,
                        },
                    })
                }

                // ❌ autres erreurs → bubble up
                throw error
            }
        }


    },
})
