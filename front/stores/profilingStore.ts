import { defineStore } from "pinia"
import { ProfileType, Question, Role } from "~/composables/types"
import { useMessageStore } from "./messageStore"
import { useApiGet } from "~~/composables/api"

export const useProfilingStore = defineStore("profiling", {
  state: () => ({
    roleById: <{ [key: string]: Role }>{},
    questionById: <{ [key: number]: Question }>{},
    orderedQuestionId: <number[]>[],
    profileTypeById: <{ [key: number]: ProfileType }>{},
    profileTypeIds: <number[]>[],
  }),
  getters: {
    roles: (state) => {
      return Object.values(state.roleById)
    },
    profileTypes: (state) => {
      return state.profileTypeIds.map((id) => state.profileTypeById[id])
    },
  },
  actions: {
    async getProfileTypes() {
      const { data, error } = await useApiGet<ProfileType[]>("profile-types/")

      if (!error.value) {
        this.profileTypeIds = []

        for (const profileType of data.value) {
          this.profileTypeById[profileType.id] = profileType
          this.profileTypeIds.push(profileType.id)
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getRoles() {
      const { data, error } = await useApiGet<Role[]>("roles/")
      if (!error.value) {
        for (const role of data.value) {
          this.roleById[role.id] = role
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getProfilingQuestions() {
      const { data, error } = await useApiGet<Question[]>(
        `profiling-questions/`,
      )
      if (error.value) {
        return false
      }
      this.orderedQuestionId = []
      for (const question of data.value) {
        this.questionById[question.id] = question
        this.orderedQuestionId.push(question.id)
      }
      return true
    },
  },
})
