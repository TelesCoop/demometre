import { defineStore } from "pinia"
import { Training } from "~/composables/types"

export const useTrainingStore = defineStore("training", {
  state: () => ({
    loaded: <boolean>false,
    trainings: <Training[]>[],
  }),
  actions: {
    async getTrainings() {
      const { data, error } = await useApiGet<Training[]>("trainings/")
      if (!error.value) {
        this.trainings = data.value!
        this.loaded = true
      }
    },
  },
})
