import { defineStore } from "pinia"
import { useApiGet } from "~~/composables/api"
import { Definition } from "~/composables/types"
import { pick } from "~/composables/tools"
import { useMessageStore } from "./messageStore"

type DefinitionResponse = Definition[]

export const useDefinitionStore = defineStore("definition", {
  state: () => ({
    definitionById: <{ [key: number]: Definition }>{},
    definitionLoaded: <boolean>false,
  }),
  getters: {
    definitionsByIdArray: () =>
      function (ids: number[]): { [key: number]: Definition } {
        return pick(this.definitionById, ids)
      },
  },
  actions: {
    async getDefinitions(): Promise<void> {
      const { data = ref<DefinitionResponse>(), error = ref() } =
        await useApiGet<DefinitionResponse>("definitions/")

      if (!error.value) {
        for (const definition of data.value) {
          this.definitionById[definition.id] = definition
        }
        this.definitionLoaded = true
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    // async getDefinitions(): Promise<{ [key: number]: Definition }> {
    //   if (!Object.keys(this.definitionById).length)
    //     return this.loadDefinitions()
    // },
  },
})
