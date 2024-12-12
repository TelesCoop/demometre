import { useUserStore } from "~/stores/userStore"

export default defineNuxtRouteMiddleware(() => {
  if (process.server) return
  const userStore = useUserStore()
  if (!userStore.isAdminOrExpertUser) {
    return navigateTo("/")
  }
})
