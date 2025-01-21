import {
  Question,
  QuestionResponse,
  QuestionResponseValue,
  QuestionType,
  SurveyType,
} from "~/composables/types"

export const QUESTION_RESPONSE_VALUE_BY_TYPE: Record<
  QuestionType,
  keyof QuestionResponseValue
> = {
  [QuestionType.UNIQUE_CHOICE]: "uniqueChoiceResponseId",
  [QuestionType.MULTIPLE_CHOICE]: "multipleChoiceResponseIds",
  [QuestionType.BOOLEAN]: "booleanResponse",
  [QuestionType.PERCENTAGE]: "percentageResponse",
  [QuestionType.NUMBER]: "numberResponse",
  [QuestionType.CLOSED_WITH_SCALE]: "closedWithScaleResponseCategories",
}
export const QUESTION_RESPONSES_BY_TYPE = {
  [SurveyType.QUESTIONNAIRE]: "responseByQuestionnaireQuestionId",
  [SurveyType.PROFILING]: "responseByProfilingQuestionId",
}

export const getQuestionResponseValue = (
  questionResponse: QuestionResponseValue | undefined,
  type: QuestionType,
) => {
  const valueName = QUESTION_RESPONSE_VALUE_BY_TYPE[type]
  const responseValue = questionResponse?.[valueName]
  if (responseValue === true) {
    return 1
  }
  if (responseValue === false) {
    return 0
  }
  return questionResponse?.[valueName]
}

export const toQuestionResponseValue = (
  value: any,
  type: QuestionType,
): QuestionResponseValue => {
  const valueName = QUESTION_RESPONSE_VALUE_BY_TYPE[type]

  return {
    [valueName]: value,
  }
}

export const getQuestionResponseString = (
  question: Question,
  questionResponse: QuestionResponse,
) => {
  const responseValue = getQuestionResponseValue(
    questionResponse,
    question.type,
  )
  let responseString = responseValue
  if (
    question.type === "unique_choice" ||
    question.type === "multiple_choice" ||
    question.type === "closed_with_scale"
  ) {
    responseString = question.responseChoices
      .filter((responseChoice) => responseChoice.id === responseValue)
      .map((responseChoice) => responseChoice.responseChoice)
      .join(", ")
  } else if (question.type === "percentage") {
    responseString = responseValue + "%"
  } else if (question.type === "boolean") {
    if (responseValue === 1) {
      return "Oui"
    }
    if (responseValue === 0) {
      return "Non"
    }
  }
  return responseString
}

export const toQuestionResponse = (
  questionId: number,
  participationId: number,
  assessmentId: number,
  hasPassed: boolean,
  response: QuestionResponseValue,
) => {
  return {
    questionId,
    participationId,
    assessmentId,
    hasPassed,
    ...response,
  }
}

export const getQuestionResponseStructure = (
  question: Question,
  response: any,
  isAnswered: boolean,
  participationId: number,
  assessmentId: number,
) => {
  const questionResponse = {
    questionId: question.id,
    participationId: participationId,
    assessmentId: assessmentId,
    hasPassed: !isAnswered,
  } as QuestionResponse

  const questionValue = QUESTION_RESPONSE_VALUE_BY_TYPE[question.type]
  questionResponse[questionValue] = response
  return questionResponse
}
