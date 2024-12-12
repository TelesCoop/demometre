import { defineStore } from "pinia"
import {
  Assessment,
  AssessmentDocumentType,
  Localities,
  RepresentativityCriteria,
  Scores,
  SurveyLocality,
  User,
} from "~/composables/types"
import { useApiDelete, useApiGet, useApiPost } from "~/composables/api"
import { useMessageStore } from "./messageStore"
import { useUserStore } from "./userStore"
import { useParticipationStore } from "./participationStore"
import { i18n } from "~/utils/i18n-util"

const $t = i18n.global.t

export const useAssessmentStore = defineStore("assessment", {
  state: () => ({
    assessmentById: <Record<number, Assessment>>{},
    assessmentsLoaded: <boolean>false,
    currentAssessmentId: <number | undefined>undefined,
    representativityCriterias: <RepresentativityCriteria[]>[],
    assessmentsWithResultsLoaded: <boolean>false,
    scoresByAssessmentId: <Record<number, Scores>>{},
    chartDataByAssessmentIdAndQuestionId: <
      {
        [key: number]: any
      }
      >{},
    expertById: <
      {
        [key: number]: User
      }
      >{},
    addingExpert: <boolean>false,
    fetchedAssessment: <Record<number, boolean>>{},
    newAssessment: <Assessment>{},
  }),
  getters: {
    assessmentTypeTitle(): string {
      return (this.currentAssessment?.municipality
        ? $t("de ma ville")
        : $t("de mon inter-communalité")
      )
    },
    assessments: (state): Assessment[] => {
      return Object.values(state.assessmentById)
    },
    assessmentsWithDetails: (state): Assessment[] => {
      return Object.values(state.assessmentById).filter(
        (ass: Assessment) => ass.details.hasDetailAccess,
      )
    },
    canSeeResultsAssessments() {
      return this.assessments.filter(
        (assessment: Assessment) =>
          assessment.publishedResults === true ||
          assessment.id === this.currentAssessmentId,
      )
    },
    currentAssessment(): Assessment {
      return this.assessmentById[this.currentAssessmentId]
    },
    experts: (state): User[] => {
      return Object.values(state.expertById)
    },
    intercommunalityAssessments() {
      return this.assessments.find(
        (assessment: Assessment) =>
          assessment.localityType === "intercommunality",
      )
    },
    myAssessments() {
      return this.assessments.filter(assessment => !!assessment?.details?.role)
    },
    userHasNoAssessment() {
      return Object.values(this.assessmentById).length == 0
    },
    userHasSingleAssessment() {
      return Object.values(this.assessmentById).length == 1
    },
    municipalityAssessments() {
      return this.assessments.find(
        (assessment: Assessment) => assessment.localityType === "municipality",
      )
    },
    representativityCriteriasForSurveyLocality() {
      return (surveyLocality: SurveyLocality) => {
        return this.representativityCriterias.filter(
          (criteria) => criteria.surveyLocality === surveyLocality,
        )
      }
    },
    userIsAssessmentInitiator() {
      return (
        this.currentAssessment?.initiatedByUser?.id === useUserStore().user.id
      )
    },
  },
  actions: {
    async addExpert(assessmentId, expertId) {
      const { data, error } = await useApiPatch<Scores>(
        `assessments/${assessmentId}/add-expert/`,
        {
          expertId,
          conditionsOfSaleConsent: this.newAssessment.conditionsOfSaleConsent,
        },
      )
      if (error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
        return false
      }
      this.assessmentById[assessmentId] = data.value
      return true
    },
    async addDocument(payload: any, assessmentId: number) {
      const { data, error } = await useApiPost<AssessmentDocumentType>(
        `assessment-documents/`,
        payload,
        $t("Impossible de téléverser le document"),
      )
      if (!error.value) {
        this.assessmentById[assessmentId].documents.push(data.value)
      }
    },
    async deleteDocument(assessmentId, assessmentDocumentId: number) {
      const { error } = await useApiDelete<Scores>(
        `assessment-documents/${assessmentDocumentId}/`,
      )
      if (error.value) {
        return false
      } else {
        console.log(
          "### remove document",
          assessmentId,
          this.assessmentById[assessmentId],
        )
        this.assessmentById[assessmentId].documents = this.assessmentById[
          assessmentId
        ].documents.filter((doc) => doc.id != assessmentDocumentId)
        return true
      }
    },
    async getAssesmentsWithPublicatedResults() {
      const { data, error } = await useApiGet<Assessment[]>(
        `assessments/published/`,
      )
      if (error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
        return false
      }
      this.assessmentsLoaded = true
      for (const assessment of data.value) {
        this.assessmentById[assessment.id] = assessment
      }
      this.assessmentsWithResultsLoaded = true
      return true
    },
    async getAssessment(id: string | number) {
      const response = await useApiGet<Assessment>(`assessments/${id}/`)

      if (response.error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(response.error.value.data?.messageCode)
        return false
      }


      this.assessmentsLoaded = true
      this.assessmentById[response.data.value.id] = response.data.value
      this.currentAssessmentId = response.data.value.id
      return true
    },
    async getAssessmentOnce(id: string | number) {
      if (!this.fetchedAssessment[id]) {
        this.fetchedAssessment[id] = true
        await this.getAssessment(id)
      }
    },
    async getAssessmentScores(assessmentId) {
      const { data, error } = await useApiGet<Scores>(
        `assessments/${assessmentId}/scores/`,
      )
      if (error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
        return false
      }
      this.scoresByAssessmentId[assessmentId] = data.value
      return true
    },
    async getAssessmentsForUser() {
      const response = await useApiGet<Assessment[]>(`assessments/mine/`)
      if (response.error.value) {
        return false
      }
      this.assessmentsLoaded = true
      for (const assessment of response.data.value!) {
        this.assessmentById[assessment.id] = assessment
      }
      if (Object.keys(this.assessmentById).length === 1) {
        const assessmentId: number = Object.keys(this.assessmentById)[0]
        this.currentAssessmentId = assessmentId
        const participationStore = useParticipationStore()
        if (
          await participationStore.getParticipationForAssessment(assessmentId)
        ) {
          await participationStore.loadAssessment(assessmentId)
        }
      }
      return true
    },
    async getChartDataByAssessmentIdAndQuestionId(
      assessmentId: number,
      questionId: number,
    ): Promise<boolean> {
      const { data, error } = await useApiGet<any>(
        `assessments/${assessmentId}/questions/${questionId}/chart-data/`,
      )
      if (error.value && error.value.data?.statusCode !== 404) {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
        return false
      }
      if (!this.chartDataByAssessmentIdAndQuestionId[assessmentId]) {
        this.chartDataByAssessmentIdAndQuestionId[assessmentId] = {}
      }
      this.chartDataByAssessmentIdAndQuestionId[assessmentId][questionId] =
        data.value
      return true
    },
    async getExperts() {
      const { data, error } = await useApiGet<User[]>(`experts/`)
      if (error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
        return false
      }
      for (const expert of data.value) {
        this.expertById[expert.id] = expert
        this.expertById[expert.id].name = this.expertById[expert.id].username
      }
      return true
    },
    async getSurveysForZipCode(zipCode: string) {
      const { data, error } = await useApiGet<Localities>(
        `surveys/by-zip-code/${parseInt(zipCode.replace(" ", ""))}/`,
      )
      if (error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
        return null
      }
      return data.value
    },
    async getOrCreateAssessment({ localityId, localityType }) {
      const { data, error } = await useApiGet<Assessment>(
        `assessments/by-locality/?locality_id=${localityId}&locality_type=${localityType}`,
      )
      if (error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
        return false
      }
      this.assessmentById[data.value.id] = data.value
      this.currentAssessmentId = data.value.id
      return true
    },
    async getRepresentativityCriterias() {
      const { data, error } = await useApiGet<RepresentativityCriteria[]>(
        "representativity-criterias/",
      )
      if (!error.value) {
        this.representativityCriterias = data.value
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async initializeAssessment(payload) {
      const { data, error } = await useApiPost<Assessment>(
        `assessments/${this.currentAssessmentId}/initialization/`,
        {
          representativityThresholds: this.representativityCriterias.map(
            (item) => {
              return { id: item.id, value: item.acceptabilityThreshold || null }
            },
          ),
          ...this.newAssessment,
          ...payload,
        },
      )
      if (error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
        return false
      }
      this.assessmentById[data.value.id] = data.value
      useParticipationStore().newParticipation.consent = true
      return true
    },
    createNewAssessment() {
      this.currentAssessmentId = undefined
    },
    onUserLogout(onlyResponses = false) {
      this.representativityCriterias = []
      this.assessmentsWithResultsLoaded = false
      this.scoresByAssessmentId = {}
      this.chartDataByAssessmentIdAndQuestionId = {}
      this.expertById = {}
      this.addingExpert = false
      if (!onlyResponses) {
        this.currentAssessmentId = undefined
        this.assessmentById = {}
        this.newAssessment = {}
      }
    },
    async saveAssessment(assessmentId: number, payload: any) {
      const { data, error } = await useApiPatch<Assessment>(
        `assessments/${assessmentId}/`,
        payload,
      )
      if (error.value) {
        return false
      }
      // after an update, experts might be a list of Ids
      let experts = data.value.experts || []
      experts = experts.map((expert: any) => {
        if (typeof expert === "number") {
          return this.expertById[expert]
        }
        return expert
      })
      data.value.experts = experts
      this.assessmentById[assessmentId] = data.value
      return true
    },
    async saveEndInitializationQuestions() {
      const { data, error } = await useApiPatch<Assessment>(
        `assessments/${this.currentAssessmentId}/questions/completed/`,
      )
      if (error.value) {
        return false
      }
      this.assessmentById[this.currentAssessmentId] = data.value
      return true
    },
  },
})
