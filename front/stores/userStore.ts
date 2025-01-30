import { defineStore } from "pinia"
import { User } from "~/composables/types"
import { useApiGet, useApiPost } from "~/composables/api"
import { useMessageStore } from "./messageStore"
import { cleanUserData, getUserData } from "~/composables/actions"
import { i18n } from "~/utils/i18n-util"

export const useUserStore = defineStore("user", {
  state: () => ({
    user: <User>{},
    afterLoginRouterGoStep: <number>-1,
  }),
  getters: {
    isLoggedOut(): boolean {
      return !this.user.email
    },
    isLoggedIn(): boolean {
      return !!this.user.email && !this.user.isUnknownUser
    },
    isUnknownUser() {
      return this.user?.isUnknownUser
    },
    isExpertUser() {
      return this.user?.isExpert
    },
    isAdminOrExpertUser() {
      return this.user?.isAdmin || this.user?.isExpert
    },
  },
  actions: {
    async createUnknownUser() {
      const { data, error } = await useApiPost<User>("auth/unknown-user")
      if (error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
        return false
      }
      this.user = data.value
    },
    async editUser(user: User) {
      const { data, error } = await useApiPatch<User>(
        "auth/edit",
        user,
        i18n.global.t("Impossible d'enregistrer les informations, les noms d'utilisateur et adresse mail doivent être uniques"),
      )
      if (!error.value) {
        this.user = data.value
        return true
      }
      return false
    },
    async login(email: string, password: string) {

      cleanUserData(true)
      const { data, error } = await useApiPost<User>(
        "auth/login",
        {
          email,
          password,
        },
        i18n.global.t("Impossible de se connecter, vérifiez vos identifiants"),
      )
      if (!error.value) {
        this.user = data.value!
        await getUserData()
        useRouter().go(this.afterLoginRouterGoStep)
      }
    },
    async signup(email: string, password: string) {
      // clean user data to reload journey after unkown user create account
      cleanUserData(true)
      const { data, error } = await useApiPost<User>("auth/signup", {
        email,
        password,
      })
      if (error.value) {
        return { error: error.value.data }
      }
      this.user = data.value
      await getUserData()

      useRouter().push("/")
    },
    async logout() {
      const { error } = await useApiPost<User>("auth/logout")
      if (!error.value) {
        this.user = { id: null, username: "", email: "" }
        cleanUserData()
        const router = useRouter()
        router.push("/login")
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async refreshProfile(showError = true) {
      const response = await useApiGet<User>(`auth/profile`)
      if (response.error.value) {
        if (showError) {
          const errorStore = useMessageStore()
          errorStore.setError(response.error.value.data?.messageCode)
        }
        return false
      }
      this.user = response.data.value
      return true
    },
    async sendResetLink(email: string) {
      const { error } = await useApiPost<User>(
        "auth/user/reset-password-link",
        {
          email,
        },
      )
      if (!error.value) {
        const router = useRouter()
        router.push("/nouveau-mdp-confirmation")
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async resetPassword(resetKey: string, password: string) {
      const { error } = await useApiPost<User>("auth/user/reset-password", {
        password,
        resetKey,
      })
      if (!error.value) {
        const router = useRouter()
        router.replace({ query: { reset_key: null } })
        router.push("/login")
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
  },
})
