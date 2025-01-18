import { defineStore } from "pinia"
import { ErrorMessages } from "~/composables/errors"

const DEFAULT_DURATION = 4000
const ERROR_DURATION = 10000

export const useMessageStore = defineStore("toast", {
  state: () => ({
    type: <string>"",
    message: <string>"",
  }),
  actions: {
    setMessage(message: string, type: string, duration: number = 0) {
      this.type = type
      this.message = message
      if (!duration) {
        duration = type === "error" ? ERROR_DURATION : DEFAULT_DURATION
      }
      setTimeout(() => {
        this.message = ""
      }, duration)
    },

    setError(messageCode: string) {
      this.setMessage(
        ErrorMessages[messageCode] || ErrorMessages.default,
        "error",
        DEFAULT_DURATION,
      )
    },
    setWarning(message: string) {
      this.setMessage(message, "warning", DEFAULT_DURATION)
    },
    setInfo(message: string) {
      this.setMessage(message, "info", DEFAULT_DURATION)
    },
  },
})
