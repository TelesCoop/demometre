import { defineStore } from "pinia"
import {
  Criteria,
  Marker,
  PillarType,
  Question,
  Survey, SurveyType,
} from "~/composables/types"
import { useMessageStore } from "./messageStore"
import { useApiGet } from "~/composables/api"

type HierarchicalQuestionStructure = {
  criteriaId: number
  markerId: number
  pillarId: number
  pillarName: string
  surveyName: string
}
export const useQuestionnaireStore = defineStore("questionnaire", {
  state: () => ({
    criteriaById: <{ [key: number]: Criteria }>{},
    isSurveyLoading: false,
    markerById: <{ [key: number]: Marker }>{},
    orderedQuestionIds: <number[]>[],
    pillarById: <{ [key: string]: PillarType }>{},
    questionById: <{ [key: number]: Question }>{},
    surveyById: <{ [key: number]: Survey }>{},
  }),
  getters: {
    getPillarByName(this) {
      return (pillarName: string) =>
        Object.values(this.pillarById).find(
          (pillar) => pillar.name === pillarName,
        )
    },
    mainSurveyId(this) {
      return Object.values(this.surveyById).find(
        (survey) => survey.surveyLocality === "city",
      )?.id!
    },
    pillarsOfSurvey() {
      return (surveyId: number) => {
        return this.surveyById[surveyId].pillars.map(
          (pillar) => this.pillarById[pillar.id],
        )
      }
    },
    pillarsOfMainSurvey(): PillarType[] {
      return this.surveyById[this.mainSurveyId].pillars.map(
        (pillar) => this.pillarById[pillar.id],
      )
    },
    questionsForSurvey() {
      return (surveyId: number): Question[] => {
        return this.surveyById[surveyId].questions.map(
          (questionId) => this.questionById[questionId],
        )
      }
    },
    getQuestionsFromIdList() {
      return (questionIds: number[]) =>
        Object.values(this.questionById).filter((question: Question) => {
          return questionIds.includes(question.id)
        }) as Question[]
    },
    getQuestionnaireQuestionByPillarName() {
      return (surveyId: number, pillarName: string): Question[] => {
        return this.questionsForSurvey(surveyId).filter(
          (question: Question) => {
            return pillarName === question.pillarName
          },
        ) as Question[]
      }
    },
    isCriteriaRelevantForAssessmentType() {
      return (assessmentType: string | undefined, criteriaId: number) => {
        if (!assessmentType) {
          return true
        }
        return this.criteriaById[criteriaId].questionIds.some((questionId) => {
          return this.questionById[questionId].assessmentTypes.includes(assessmentType)
        })
      }
    },
    isMarkerRelevantForAssessmentType() {
      return (assessmentType: string | undefined, markerId: number) => {
        if (!assessmentType) {
          return true
        }
        return this.markerById[markerId].criteriaIds.some((criteriaId) => {
          return this.isCriteriaRelevantForAssessmentType(assessmentType, criteriaId)
        })
      }
    },
  },
  actions: {
    getPillarNameById(pillarId: number) {
      return this.pillarById[pillarId].name
    },
    async getSurvey(surveyId: number) {
      const { data, error } = await useApiGet<Survey[]>(
        `surveys/${surveyId}/`,
        "",
        `survey-${surveyId}`,
      )
      if (!error.value) {
        const survey: Survey = data.value!
        for (const pillar of survey.pillars) {
          this.pillarById[pillar.id] = pillar
          for (const marker of pillar.markers) {
            this.markerById[marker.id] = marker
            for (const criteria of marker.criterias) {
              this.criteriaById[criteria.id] = criteria
            }
          }
        }
        this.surveyById[survey.id] = survey
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getSurveysSetup() {
      const { data, error } = await useApiGet<{
        surveys: Survey[]
        questions: Question[]
      }>("surveys/all/")
      if (!error.value) {
        const surveys = data.value.surveys
        this.surveyById = {}
        this.pillarById = {}
        this.markerById = {}
        this.criteriaById = {}
        for (const survey of surveys) {
          survey.questions = []
          for (const pillar of survey.pillars) {
            this.pillarById[pillar.id] = pillar
            for (const marker of pillar.markers) {
              this.markerById[marker.id] = marker
              for (const criteria of marker.criterias) {
                this.criteriaById[criteria.id] = criteria
              }
            }
          }
          this.surveyById[survey.id] = survey
        }

        const questions = data.value.questions
        for (const question of questions) {
          this.questionById[question.id] = question
          this.surveyById[question.surveyId].questions.push(question.id)
        }
      } else {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
      }
    },
    async getQuestionsForSurvey(surveyId: number) {
      const { data, error } = await useApiGet<Question[]>(
        `surveys/${surveyId}/questions/`,
      )
      if (error.value) {
        const errorStore = useMessageStore()
        errorStore.setError(error.value.data?.messageCode)
        return false
      }
      const orderedQuestionIds = []

      for (const question of data.value!) {
        this.questionById[question.id] = question
        orderedQuestionIds.push(question.id)
      }
      this.surveyById[surveyId].questions = orderedQuestionIds
      return true
    },
    getHierarchicalQuestionStructure({
      question,
      questionId,
    }: {
      question?: Question
      questionId?: number
    }): HierarchicalQuestionStructure | undefined {
      const currentQuestion = question || this.questionById[questionId]

      if (!currentQuestion.criteriaId) {
        return
      }

      const criteria = this.criteriaById[currentQuestion.criteriaId]
      const marker = this.markerById[criteria.markerId]
      const pillar = this.pillarById[marker.pillarId]
      const survey = this.surveyById[pillar.surveyId]
      return {
        criteriaId: criteria.id,
        markerId: marker.id,
        pillarId: marker.pillarId,
        pillarName: marker.pillarName,
        surveyName: survey.name,
        surveyId: survey.id,
      }
    },
  },
})
