import { defineStore } from "pinia"
import { Localities } from "~/composables/types"

export const useExportStore = defineStore("export", () => {
  const data = ref<{
    location?: Localities
    role?: number
  }>({
    location: undefined,
    role: undefined,
  })

  return { data }
})
