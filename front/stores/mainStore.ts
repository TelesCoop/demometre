import { defineStore } from "pinia"
import { doNothing } from "~/utils/util"

export const useMainStore = defineStore("main", {
  state: () => ({
    confirmation: {
      confirmationLabel: "",
      onCancel: process.server ? null : doNothing,
      onConfirm: process.server ? null : doNothing,
      text: "",
      title: "",
    },
  }),
  actions: {
    resetConfirm() {
      this.confirmation = {
        confirmationLabel: "",
        onCancel: doNothing,
        onConfirm: doNothing,
        text: "",
        title: "",
      }
    },
  },
})
