import { Scores } from "~/composables/types"
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { isNullOrUndefined } from "assets/utils"

const IS_STRENGHT_OR_IMPROVEMENT = {
  1: "improvements",
  2: "improvements",
  3: "strengths",
  4: "strengths",
}
const ASSESSMENT_SCORE_BY_SUB_LEVEL = {
  pillar: "byMarkerId",
  marker: "byCriteriaId",
}
const QUESTIONNAIRE_STORE_SUB_LEVEL = {
  pillar: "markerById",
  marker: "criteriaById",
}

export const getScoreToDisplay = (score: number | null) => {
  if (isNullOrUndefined(score)) {
    return null
  }
  if (score < 0.25) {
    return 1
  }
  if (score < 0.5 && score >= 0.25) {
    return 2
  }
  if (score < 0.75 && score >= 0.5) {
    return 3
  }
  if (score >= 0.75) {
    return 4
  }
}

export const getStrenghtAndImprovements = (
  assessmentScores: Scores,
  listIds: number[],
  level: string,
) => {
  const questionnaireStore = useQuestionnaireStore()
  const strenghtsAndImprovements = { strengths: [], improvements: [] }
  for (const itemId of listIds) {
    if (assessmentScores[ASSESSMENT_SCORE_BY_SUB_LEVEL[level]][itemId]) {
      const scoreToDisplay = getScoreToDisplay(
        assessmentScores[ASSESSMENT_SCORE_BY_SUB_LEVEL[level]][itemId],
      )
      strenghtsAndImprovements[IS_STRENGHT_OR_IMPROVEMENT[scoreToDisplay]].push(
        questionnaireStore[QUESTIONNAIRE_STORE_SUB_LEVEL[level]][itemId].name,
      )
    }
  }
  return strenghtsAndImprovements
}
