import { defineStore } from "pinia"
import { RgpdSettings, StructureSettings } from "~/composables/types"
import { useApiGet } from "~~/composables/api"
import { useMessageStore } from "./messageStore"

export const useSettingStore = defineStore("setting", {
  state: () => ({
    rgpdSettings: <RgpdSettings>{},
    rgpdSettingsLoaded: <boolean>false,
    structureSettings: <StructureSettings>{},
  }),
  actions: {
    async getRgpdSettings() {
      const { data, error } = await useApiGet<RgpdSettings[]>("rgpd-settings/")
      if (!error.value) {
        if (data.value.length) {
          this.rgpdSettings = data.value[0]
        } else {
          console.error("Impossible to retrieve settings")
        }
        this.rgpdSettingsLoaded = true
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getStructureSettings() {
      const { data, error } = await useApiGet<StructureSettings[]>(
        "structure-settings/",
      )
      if (!error.value) {
        if (data.value.length) {
          this.structureSettings = data.value[0]
        } else {
          console.error("Impossible to retrieve settings")
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
  },
})
