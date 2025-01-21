import { defineStore } from "pinia"
import {
  Objectivity,
  Question,
  QuestionResponse,
  Workshop,
  WorkshopParticipation,
} from "~/composables/types"
import { useMessageStore } from "./messageStore"
import { i18n } from "~/utils/i18n-util"

const $t = i18n.global.t

type FullWorkshop = Workshop & {
  participations: WorkshopParticipation[]
  assessmentResponses: QuestionResponse[]
}

export const useWorkshopStore = defineStore("workshop", {
  state: () => ({
    allAssessmentsLoaded: <boolean>false,
    assessmentResponseByQuestionIdByWorkshopId: <
      { [key: number]: { [key: number]: QuestionResponse } }
      >{},
    isDirtyByParticipationIdByQuestionId: <Record<number, Record<number, boolean>>>{},
    participationById: <Record<number, WorkshopParticipation>>{},
    workshopById: <Record<number, Workshop>>{},
    workshopsLoadedByAssessments: <Record<number, boolean>>{},

  }),
  getters: {
    isDirty: (state) => {
      return (participationId: number, questionId: number): boolean => {
        return !!(state.isDirtyByParticipationIdByQuestionId[participationId] || {})[questionId]
      }
    },
    workshops: (state) => {
      return Object.values(state.workshopById)
    },
    workshopParticipations: (state) => {
      return (workshopId: number, filterMedium = ""): WorkshopParticipation[] => {
        const workshop = state.workshopById[workshopId]
        if (workshop == null) {
          return []
        }
        const toReturn: WorkshopParticipation[] = workshop.participationIds!.map(
          (participationId) => state.participationById[participationId],
        ).filter(el => el != null)
        if (filterMedium) {
          return toReturn.filter((participation: WorkshopParticipation) => participation.medium === filterMedium)
        }
        return toReturn
      }
    },
  },
  actions: {
    async closeWorkshop(workshopId: number) {
      const { data, error } = await useApiPatch<Workshop>(
        `workshops/${workshopId}/closed/`,
      )
      const messageStore = useMessageStore()
      if (error.value) {
        messageStore.setError(error.value.data?.messageCode)
        return false
      }
      const workshop = data.value
      this.workshopById[workshop.id] = workshop
      this.workshopById[workshop.id].changed = false
      return true
    },
    async createOrUpdateParticipation(
      participation: WorkshopParticipation,
      workshopId: number,
      assessmentId: number,
    ) {
      console.log("### createOrUpdateParticipation", participation, workshopId)
      participation.responses = Object.values(
        { ...participation.responseByQuestionId },
      )
      const { data, error } = await useApiPost<WorkshopParticipation>(
        `workshops/${workshopId}/participation/`,
        { ...participation, workshopId: workshopId, assessmentId: assessmentId },
      )
      if (!error.value) {
        this.setParticipationtFromApiToStore(data.value)
        if (
          !this.workshopById[workshopId].participationIds.includes(
            data.value.id,
          )
        ) {
          this.workshopById[workshopId].participationIds.push(data.value.id)
        }
        return data.value
      }

      messageStore.setError(error.value.data?.messageCode)
      return false
    },
    async createOrUpdateQuestionnaireResponses(
      workshopId: number,
      question: Question,
    ) {
      let errorOccured = false
      if (question.objectivity === Objectivity.OBJECTIVE) {
        const apiResponse = await useApiPost<QuestionResponse>(
          `assessment-responses/`,
          this.assessmentResponseByQuestionIdByWorkshopId[workshopId][
            question.id
          ],
        )
        if (apiResponse.error.value) {
          errorOccured = true
        }
      } else {
        for (const participationId of this.workshopById[workshopId].participationIds) {
          const response =
            this.participationById[participationId].responseByQuestionId[
              question.id
            ]

          if (response && Object.entries(response).length !== 0) {
            const apiResponse = await useApiPost<QuestionResponse>(
              `workshops/${workshopId}/participation/${participationId}/response/`,
              response,
            )
            if (apiResponse.error.value) {
              errorOccured = true
            }
          }
        }
      }
      const messageStore = useMessageStore()

      if (errorOccured) {
        messageStore.setError($t("Une erreur s'est produite lors de la sauvegarde"))
        return false
      }
      messageStore.setInfo($t("Sauvegarde réussie"))
      return true
    },
    async createOrUpdateWorkshop(workshop: Workshop) {
      const {
        data,
        error,
      } = await useApiPost<Workshop>(`workshops/`, workshop, $t("Impossible d'ajouter l'atelier"))
      if (!error.value) {
        this.workshopById[data.value.id] = data.value
        return true
      }
      const errorStore = useMessageStore()
      errorStore.setError(error.value?.data?.messageCode)
      return false
    },
    async getWorkshop(workshopId: number) {
      const { data, error } = await useApiGet<FullWorkshop>(
        `full-workshops/${workshopId}/`,
      )
      if (!error.value) {
        this.setFullWorkshopFromApiToStore(data.value)
      }
    },
    async deleteParticipation(participationId: number) {
      const workshopId = this.participationById[participationId].workshopId
      if (!workshopId) {
        useMessageStore().setMessage($t("Impossible de supprimer le participant (impossible de récupérer son atelier)"), "error")
        return false
      }
      const { error } = await useApiDelete(
        `workshops/participation/${participationId}/`,
        $t("Impossible de supprimer le participant"),
      )
      if (error.value) {
        return false
      }
      delete this.participationById[participationId]
      this.workshopById[workshopId].participationIds = this.workshopById[workshopId].participationIds!.filter(id => id !== participationId)

      return true
    },
    async getWorkshopsForAssessment(assessmentId: number) {
      const { data, error } = await useApiGet<Workshop[]>(`workshops/by-assessment/${assessmentId}/`)
      if (!error.value) {
        for (const workshop of data.value) {
          this.workshopById[workshop.id] = workshop
          this.workshopById[workshop.id].changed = false
        }
        this.workshopsLoadedByAssessments[assessmentId] = true
      }
    },
    async saveWorkshop(workshopId: number, payload: any) {
      const { data, error } = await useApiPatch<Workshop>(
        `workshops/${workshopId}/`, payload,
      )
      if (error.value) {
        return false
      }
      this.workshopById[workshopId] = data.value
      return true
    },
    markDirty(participationId: number, questionId: number, dirty = true) {
      if (this.isDirtyByParticipationIdByQuestionId[participationId] == null) {
        this.isDirtyByParticipationIdByQuestionId[participationId] = {}
      }
      this.isDirtyByParticipationIdByQuestionId[participationId][questionId] = dirty
    },
    setFullWorkshopFromApiToStore(workshop: FullWorkshop) {
      this.workshopById[workshop.id] = workshop
      this.workshopById[workshop.id].changed = false
      workshop.participations.forEach((participation) => {
        this.setParticipationtFromApiToStore(participation)
      })
      this.assessmentResponseByQuestionIdByWorkshopId[workshop.id] = {}
      workshop.assessmentResponses.forEach((response) => {
        this.assessmentResponseByQuestionIdByWorkshopId[workshop.id][
          response.questionId
        ] = response
      })
    },
    setParticipationtFromApiToStore(participation: WorkshopParticipation) {
      participation.changed = false
      participation.responseByQuestionId = {}
      participation.responses.forEach((response) => {
        participation.responseByQuestionId[response.questionId] = response
      })
      this.participationById[participation.id] = participation
    },
  },
})
