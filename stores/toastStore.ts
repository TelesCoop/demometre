import { defineStore } from "pinia"

export const useToastStore = defineStore("toast", {
  state: () => ({
    type: <string>"",
    message: <string>"",
  }),
  actions: {
    setError(message: string) {
      this.type = "error"
      this.message = message
      setTimeout(() => {
        this.message = ""
      }, 4000)
    },
    setWarning(message: string) {
      this.type = "warning"
      this.message = message
    },
  },
})