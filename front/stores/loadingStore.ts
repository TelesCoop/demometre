import { defineStore } from "pinia"

export const useLoadingStore = defineStore("loading", {
  state: () => <{ [key: string]: "loading" | "done" | "error" }>{},
  actions: {
    markLoading(key: string) {
      this.$patch({ [key]: "loading" })
    },
    markDone(key: string) {
      this.$patch({ [key]: "done" })
    },
    markError(key: string) {
      this.$patch({ [key]: "error" })
    },
  },
  getters: {
    isLoading: (state) => {
      return (key: string) => state[key] === "loading"
    },
  },
})
