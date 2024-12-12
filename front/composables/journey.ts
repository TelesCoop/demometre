import { computed, getCurrentInstance } from "vue"
import { useProfilingStore } from "~/stores/profilingStore"
import { Assessment, Objectivity, Participation, Question, SurveyType } from "~/composables/types"
import { useParticipationStore } from "~/stores/participationStore"
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { useUserStore } from "~/stores/userStore"

type QuestionDataFilter = {
  question: Question
  participation: Participation | undefined
  assessment: Assessment
}
const QUESTION_FILTERS = {
  role({ question, participation }: QuestionDataFilter): boolean {
    return question.roleIds.includes(participation.roleId)
  },
  population({ question, assessment }: QuestionDataFilter) {
    const population =
      assessment?.municipality?.population || assessment?.epci?.population || 0
    return (
      (!question.populationLowerBound ||
        question.populationLowerBound <= population) &&
      (!question.populationUpperBound ||
        question.populationUpperBound >= population)
    )
  },
  profile({ question, participation }: QuestionDataFilter): boolean {
    return (
      !question.profileIds?.length ||
      question.profileIds.some((profileId) =>
        participation.profileIds.includes(profileId),
      )
    )
  },
  assessmentType({ question, assessment }: QuestionDataFilter) {
    return (
      !question.assessmentTypes ||
      question.assessmentTypes?.includes(assessment?.assessmentType)
    )
  },
}

const QUESTION_FILTERS_VALUES = Object.values(QUESTION_FILTERS)

const OPERATORS_STRATEGY = {
  or: "some",
  and: "every",
}

const NUMERICAL_OPERATOR_STRATEGY = {
  "<": (x, y) => {
    return x < y
  },
  ">": (x, y) => {
    return x > y
  },
  "<=": (x, y) => {
    return x <= y
  },
  ">=": (x, y) => {
    return x >= y
  },
  "!=": (x, y) => {
    return x !== y
  },
  "=": (x, y) => {
    return x === y
  },
}

const RULES_STRATEGY = {
  unique_choice: ({ response }): boolean => {
    return Boolean(
      rule.responseChoiceIds?.includes(response?.uniqueChoiceResponseId),
    )
  },
  multiple_choice: ({ rule, response }): boolean => {
    return Boolean(
      rule.responseChoiceIds?.some((item) =>
        response?.multipleChoiceResponseIds?.includes(item),
      ),
    )
  },
  boolean: ({ rule, response }): boolean => {
    return Boolean(rule.booleanResponse === response.booleanResponse)
  },
  percentage: ({ rule, response }): boolean => {
    return Boolean(
      NUMERICAL_OPERATOR_STRATEGY[rule.numericalOperator]?.(
        response.percentageResponse,
        rule.numericalValue,
      ),
    )
  },
  closed_with_scale: (): boolean => {
    return true
  },
}

function isRelevant(question: Question, data) {
  const operator: string =
    OPERATORS_STRATEGY[question.rulesIntersectionOperator]
  return question.rules[operator]((rule) => {
    const response = data.responseByQuestionId[rule.conditionalQuestionId]
    return RULES_STRATEGY[rule.type]({ rule, response })
  })
}

export function useProfilingJourney() {
  const vm = getCurrentInstance()
  const assessmentStore = useAssessmentStore()

  const journey = computed(() => {
    const profilingStore = useProfilingStore()
    const participationStore = useParticipationStore()
    const participation = participationStore.participation
    const assessment = assessmentStore.currentAssessment
    if (assessment == null) {
      return []
    }

    const responseByQuestionId =
      participationStore.responseByProfilingQuestionId
    const questionIds = profilingStore.orderedQuestionId
      .filter((questionId) => {
        const question = profilingStore.questionById[questionId]
        // this test is here instead of QUESTION_FILTERS_VALUES because it only
        // applies to profiling questions
        if (!question.surveys.includes(assessment.surveyId)) {
          return false
        }
        return QUESTION_FILTERS_VALUES.every((test) =>
          test({ question, participation, assessment }),
        )
      })
      .filter((questionId) => {
        const question = profilingStore.questionById[questionId]
        return isRelevant.bind(vm)(question, { responseByQuestionId })
      })
    return questionIds
  })
  const nextQuestionId = (
    currentQuestionId: number,
    nextQuestion: boolean,
  ): number => {
    const myJourney = journey.value
    const index = myJourney.indexOf(currentQuestionId)
    return nextQuestion ? myJourney[index + 1] : myJourney[index - 1]
  }

  const goToNextQuestion = (currentQuestionId: number) => {
    if (isLastQuestion(currentQuestionId)) {
      useRouter().push(`/evaluation/${assessmentStore.currentAssessmentId}/affinage/validation`)
    } else {
      const questionId = nextQuestionId(currentQuestionId, true)
      useRouter().push(`/evaluation/${assessmentStore.currentAssessmentId}/affinage/${questionId}`)
    }
  }

  const goToPreviousQuestion = (currentQuestionId: number) => {
    if (!isFirstQuestion(currentQuestionId)) {
      const questionId = nextQuestionId(currentQuestionId, false)
      useRouter().push(`/evaluation/${assessmentStore.currentAssessmentId}/affinage/${questionId}`)
    }
  }

  const isLastQuestion = (currentQuestionId: number): boolean => {
    const myJourney = journey.value
    const index = myJourney.indexOf(currentQuestionId)
    return index + 1 === myJourney.length
  }

  const isFirstQuestion = (currentQuestionId: number): boolean => {
    const myJourney = journey.value
    return myJourney.indexOf(currentQuestionId) === 0
  }

  const surveyType = (): SurveyType => {
    return SurveyType.PROFILING
  }

  return {
    journey,
    nextQuestionId,
    goToNextQuestion,
    goToPreviousQuestion,
    isLastQuestion,
    isFirstQuestion,
    surveyType,
  }
}

export function useQuestionnaireJourney(pillarName: string) {
  const assessmentStore = useAssessmentStore()

  const journey = computed(() => {
    const questionnaireStore = useQuestionnaireStore()
    const participationStore = useParticipationStore()
    const userStore = useUserStore()

    const participation = participationStore.participation
    const assessment = assessmentStore.currentAssessment
    if (assessment == null) {
      return []
    }

    return questionnaireStore
      .getQuestionnaireQuestionByPillarName(assessment.surveyId, pillarName)
      .filter((question: Question) => {
        return (
          QUESTION_FILTERS_VALUES.every((test) =>
            test({ question, participation, assessment }),
          ) &&
          (question.objectivity === Objectivity.SUBJECTIVE ||
            userStore.isLoggedIn)
        )
      })
      .map((question: Question) => question.id)
  })
  const nextQuestionId = (
    currentQuestionId: number,
    nextQuestion: boolean,
  ): number => {
    const myJourney = journey.value
    const index = myJourney.indexOf(currentQuestionId)
    return nextQuestion ? myJourney[index + 1] : myJourney[index - 1]
  }

  const goToNextQuestion = (currentQuestionId: number) => {
    if (isLastQuestion(currentQuestionId)) {
      useRouter().push(`/evaluation/${assessmentStore.currentAssessmentId}/questionnaire`)
    } else {
      const questionId = nextQuestionId(currentQuestionId, true)
      useRouter().push({
        path: `/evaluation/${assessmentStore.currentAssessmentId}/questionnaire/${questionId}`,
        query: { pillar: pillarName },
      })
    }
  }

  const goToPreviousQuestion = (currentQuestionId: number) => {
    if (isFirstQuestion(currentQuestionId)) {
      useRouter().push(`/evaluation/${assessmentStore.currentAssessmentId}/questionnaire`)
    } else {
      const questionId = nextQuestionId(currentQuestionId, false)
      useRouter().push({
        path: `/evaluation/${assessmentStore.currentAssessmentId}/questionnaire/${questionId}`,
        query: { pillar: pillarName },
      })
    }
  }

  const isLastQuestion = (currentQuestionId: number): boolean => {
    const myJourney = journey.value
    const index = myJourney.indexOf(currentQuestionId)
    return index + 1 === myJourney.length
  }

  const isFirstQuestion = (currentQuestionId: number): boolean => {
    const myJourney = journey.value
    return myJourney.indexOf(currentQuestionId) === 0
  }

  const surveyType = (): SurveyType => {
    return SurveyType.QUESTIONNAIRE
  }

  return {
    journey,
    nextQuestionId,
    goToNextQuestion,
    goToPreviousQuestion,
    isLastQuestion,
    isFirstQuestion,
    surveyType,
  }
}

export function useInitializationJourney() {
  const questionnaireStore = useQuestionnaireStore()
  const assessmentStore = useAssessmentStore()

  const journey = computed(() => {
    // returns a list of question IDs for current assessment, in the right order
    if (assessmentStore.currentAssessment == null) {
      return []
    }
    return questionnaireStore.questionsForSurvey(assessmentStore.currentAssessment.surveyId, "useInitializationJourney")
      .filter((question: Question) => {
        const assessment = assessmentStore.currentAssessment
        const participation = undefined
        return (
          QUESTION_FILTERS.population({
            question,
            participation,
            assessment,
          }) &&
          QUESTION_FILTERS.assessmentType({
            question,
            participation,
            assessment,
          }) &&
          question.objectivity === Objectivity.OBJECTIVE
        )
      })
      .map((question: Question) => question.id)
  })
  const nextQuestionId = (
    currentQuestionId: number,
    nextQuestion: boolean,
  ): number => {
    const myJourney = journey.value
    const index = myJourney.indexOf(currentQuestionId)
    return nextQuestion ? myJourney[index + 1] : myJourney[index - 1]
  }

  const goToNextQuestion = (currentQuestionId: number) => {
    const assessmentStore = useAssessmentStore()
    if (isLastQuestion(currentQuestionId)) {
      useRouter().push({
        path: `/evaluation/initialisation/${assessmentStore.currentAssessmentId}/validation`,
      })
    } else {
      const questionId = nextQuestionId(currentQuestionId, true)
      useRouter().push({
        path: `/evaluation/initialisation/${assessmentStore.currentAssessmentId}/questions-objectives/${questionId}`,
      })
    }
  }

  const goToPreviousQuestion = (currentQuestionId: number) => {
    const assessmentStore = useAssessmentStore()
    if (isFirstQuestion(currentQuestionId)) {
      useRouter().push(
        `/evaluation/initialisation/${assessmentStore.currentAssessmentId}/questions-objectives`,
      )
    } else {
      const questionId = nextQuestionId(currentQuestionId, false)
      useRouter().push({
        path: `/evaluation/initialisation/${assessmentStore.currentAssessmentId}/questions-objectives/${questionId}`,
      })
    }
  }

  const isLastQuestion = (currentQuestionId: number): boolean => {
    const myJourney = journey.value
    const index = myJourney.indexOf(currentQuestionId)
    return index + 1 === myJourney.length
  }

  const isFirstQuestion = (currentQuestionId: number): boolean => {
    const myJourney = journey.value
    return myJourney.indexOf(currentQuestionId) === 0
  }

  const surveyType = (): SurveyType => {
    return SurveyType.INITILIZATION
  }

  return {
    journey,
    nextQuestionId,
    goToNextQuestion,
    goToPreviousQuestion,
    isLastQuestion,
    isFirstQuestion,
    surveyType,
  }
}

export const getLastQuestionIdOfJourney = (responses, journey) => {
  const answeredQuestionIds = Object.keys(responses)
  const index = journey.findIndex(
    (questionId) => !answeredQuestionIds.includes(questionId.toString()),
  )

  const isLast = index === -1

  return {
    lastQuestionId: isLast ? journey[journey.length] : journey[index - 1],
    isLast: isLast,
  }
}

export const getLastAnsweredProfilingQuestionId = () => {
  const participationStore = useParticipationStore()
  const profilingJourney = useProfilingJourney()

  return getLastQuestionIdOfJourney(
    participationStore.responseByProfilingQuestionId,
    profilingJourney.journey.value,
  ).lastQuestionId
}

export const getLastQuestionOfPillar = (pillarName: string) => {
  const participationStore = useParticipationStore()
  const questionnaireJourney = useQuestionnaireJourney(pillarName)

  return getLastQuestionIdOfJourney(
    participationStore.responseByQuestionnaireQuestionId,
    questionnaireJourney.journey.value,
  )
}
