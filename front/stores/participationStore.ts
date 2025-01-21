import { defineStore } from "pinia"
import { useApiGet, useApiPatch, useApiPost } from "~/composables/api"
import {
  Objectivity,
  Participation,
  PillarName,
  Question,
  QuestionResponse,
  QuestionResponseValue,
  SurveyType,
} from "~/composables/types"
import { useAssessmentStore } from "./assessmentStore"
import {
  QUESTION_RESPONSES_BY_TYPE,
  toQuestionResponse,
} from "~/utils/question-response"
import { useUserStore } from "./userStore"
import { useMessageStore } from "./messageStore"
import { useQuestionnaireStore } from "./questionnaireStore"

type Status = {
  total: number
  answered: number
  completed: boolean
  participated?: boolean
}

export const useParticipationStore = defineStore("participation", {
  state: () => ({
    currentParticipationId: -1,
    currentlyLoadedSubjectiveResponsesAssessmentId: -1,
    currentlyLoadedProfilingResponsesAssessmentId: -1,
    launchedParticipations: <Record<number, boolean>>{},
    fetchedParticipations: <Record<number, boolean>>{},
    launchedLoadParticipations: <Record<number, boolean>>{},
    fetchedLoadParticipations: <Record<number, boolean>>{},
    profilingCurrent: <number[]>[],
    responseByProfilingQuestionId: <
      {
        [key: number]: QuestionResponse
      }
    >{},
    responseByQuestionnaireQuestionId: <
      {
        [key: number]: QuestionResponse
      }
    >{},
    newParticipation: <Participation>{},
    participations: <
      {
        [key: number]: Participation
      }
    >{},
    showCancelParticipationModal: <boolean>false,
    showSaveParticipationModal: <boolean>false,
    totalAndAnsweredQuestionsByPillarName: <Record<string, Status>>{},
  }),
  getters: {
    participation: (state): Participation | {} => {
      return state.participations?.[state.currentParticipationId] || {}
    },
    id(): Participation["id"] | undefined {
      return "id" in this.participation ? this.participation.id : undefined
    },
    hasAnsweredQuestionnaireQuestion: (state) => {
      return (questionId: number) => {
        return state.responseByQuestionnaireQuestionId[questionId]
          ? true
          : false
      }
    },
    status(): Status {
      let total = 0
      let answered = 0
      for (const st of Object.values(
        this.totalAndAnsweredQuestionsByPillarName,
      )) {
        total += st.total
        answered += st.answered
      }
      return {
        total,
        answered,
        completed: total === answered,
        participated: answered > 0,
      }
    },
  },
  actions: {
    // Create participation only one time
    async createParticipation() {
      const userStore = useUserStore()
      // If user not authenticated, create anonymous user
      if (!userStore.isLoggedIn && !userStore.isUnknownUser) {
        await userStore.createUnknownUser()
      }
      const { data, error } = await useApiPost<Participation>(
        "participations/",
        {
          assessmentId: useAssessmentStore().currentAssessmentId,
          roleId: this.newParticipation.roleId,
          consent: this.newParticipation.consent,
        },
      )
      if (!error.value) {
        this.currentParticipationId = data.value.id
        this.participations[this.currentParticipationId] = data.value
        return true
      }
      const errorStore = useMessageStore()
      errorStore.setError(error.value.data?.messageCode)
      return false
    },
    async getParticipationForAssessment(
      assessmentId: number,
    ): Promise<boolean> {
      const response = await useApiGet<Participation>(
        `participations/by-assessment/${assessmentId}/`,
      )
      if (response.error.value) {
        return false
      }
      if (response.data.value?.id) {
        this.currentParticipationId = response.data.value.id
        this.participations[this.currentParticipationId] = response.data.value
      }

      return true
    },
    async getParticipationForAssessmentOnce(
      assessmentId: number,
    ): Promise<boolean> {
      if (this.launchedParticipations[assessmentId]) {
        return true
      }
      this.launchedParticipations[assessmentId] = true
      const toReturn = await this.getParticipationForAssessment(assessmentId)
      this.fetchedParticipations[assessmentId] = true
      return toReturn
    },
    async getParticipations(): Promise<boolean> {
      const response = await useApiGet<Participation[]>("participations")
      if (response.error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(response.error.value.data?.messageCode)
        return false
      }
      this.participations = response.data.value

      return true
    },
    chooseRole(roleId) {
      this.newParticipation.roleId = roleId
    },
    async getProfilingQuestionResponsesForAssessment(assessmentId: number) {
      const response = await useApiGet<QuestionResponse[]>(
        `participation-responses/by-assessment/${assessmentId}/?context=profiling`,
      )
      if (response.error.value) {
        return false
      }

      response.data.value.forEach((item) => {
        this.responseByProfilingQuestionId[item.questionId] = item
        this.currentlyLoadedProfilingResponsesAssessmentId = assessmentId
      })
      return true
    },
    async getQuestionnaireSubjectiveQuestionResponsesForAssessment(
      assessmentId: number,
    ) {
      const participationResponses = await useApiGet<QuestionResponse[]>(
        `participation-responses/by-assessment/${assessmentId}/?context=questionnaire`,
      )
      if (
        participationResponses.error.value ||
        !participationResponses.data.value
      ) {
        return false
      }
      participationResponses.data.value.forEach((item) => {
        this.responseByQuestionnaireQuestionId[item.questionId] = item
        this.currentlyLoadedSubjectiveResponsesAssessmentId = assessmentId
      })
      return true
    },
    async getQuestionnaireObjectiveQuestionResponsesForAssessment(
      assessmentId: number,
    ) {
      const assessmentResponses = await useApiGet<QuestionResponse[]>(
        `assessment-responses/by-assessment/${assessmentId}/`,
      )
      if (assessmentResponses.error.value) {
        return false
      }
      const responses = <QuestionResponse[]>assessmentResponses!.data.value
      responses.forEach((item) => {
        this.responseByQuestionnaireQuestionId[item.questionId] = item
      })
      return true
    },
    async loadAssessment(assessmentId: number) {
      await Promise.all([
        this.getProfilingQuestionResponsesForAssessment(assessmentId),
        this.getQuestionnaireSubjectiveQuestionResponsesForAssessment(
          assessmentId,
        ),
        this.getQuestionnaireObjectiveQuestionResponsesForAssessment(
          assessmentId,
        ),
      ])
    },
    async loadAssessmentOnce(assessmentId: number) {
      if (this.launchedLoadParticipations[assessmentId]) {
        return
      }
      this.launchedLoadParticipations[assessmentId] = true
      await this.loadAssessment(assessmentId)
      this.fetchedLoadParticipations[assessmentId] = true
    },
    newAssessment() {
      this.responseByProfilingQuestionId = {}
      this.responseByQuestionnaireQuestionId = {}
      this.totalAndAnsweredQuestionsByPillarName = {}
    },
    async saveResponse(
      question: Question,
      response: QuestionResponseValue,
      isAnswered: boolean,
    ) {
      const questionResponse = toQuestionResponse(
        question.id,
        this.id!,
        useAssessmentStore().currentAssessmentId!,
        !isAnswered,
        response,
      )

      let apiResponse
      if (
        question.objectivity === Objectivity.OBJECTIVE &&
        question.surveyType === SurveyType.QUESTIONNAIRE
      ) {
        apiResponse = await useApiPost<QuestionResponse>(
          `assessment-responses/`,
          questionResponse,
        )
      } else {
        apiResponse = await useApiPost<QuestionResponse>(
          "participation-responses/",
          questionResponse,
        )
      }
      const { data, error } = apiResponse

      if (error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
      if (!error.value && data.value) {
        const questionResponses =
          this[QUESTION_RESPONSES_BY_TYPE[question.surveyType]]
        questionResponses[question.id] = data.value
        if (question.surveyType === SurveyType.QUESTIONNAIRE) {
          this.setTotalAndAnsweredQuestionsInPillar(question.pillarName)
        }
        return true
      }
      return false
    },

    async saveEndQuestionnaire(
      isProfilingQuestion: boolean,
      pillarId?: number,
    ) {
      const payload = {
        profilingQuestion: isProfilingQuestion,
        pillarId: pillarId,
      }
      const { data, error } = await useApiPatch<Participation>(
        `participations/${this.id}/questions/completed/`,
        payload,
      )
      if (error.value) {
        return false
      }
      this.participations[this.currentParticipationId] = data.value
      return true
    },
    onUserLogout() {
      this.responseByProfilingQuestionId = {}
      this.responseByQuestionnaireQuestionId = {}
      this.profilingCurrent = []
      this.participations = {}
      this.newParticipation = {}
      this.currentParticipationId = undefined
      this.totalAndAnsweredQuestionsByPillarName = {}
    },
    setTotalAndAnsweredQuestionsInPillar(pillarName: string) {
      const journey = useQuestionnaireJourney(pillarName)
      const questions = useQuestionnaireStore().getQuestionsFromIdList(
        journey.journey.value,
      )
      const answered = questions.reduce(
        (totalAnswered, question: Question) =>
          totalAnswered + this.hasAnsweredQuestionnaireQuestion(question.id),
        0,
      )

      this.totalAndAnsweredQuestionsByPillarName[pillarName] = {
        total: questions.length,
        answered: answered,
        completed:
          questions.length === 0 ? true : answered / questions.length === 1,
      }
    },
    setTotalAndAnsweredQuestionsByPillarName() {
      this.totalAndAnsweredQuestionsByPillarName = {}
      for (const pillarName in PillarName) {
        this.setTotalAndAnsweredQuestionsInPillar(PillarName[pillarName])
      }
    },
    setShowCancelParticipationModal(show) {
      this.showCancelParticipationModal = show
    },
    setShowSaveParticipationModal(show) {
      this.showSaveParticipationModal = show
    },
  },
})
