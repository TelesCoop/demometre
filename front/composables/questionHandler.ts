import { computed } from "vue"
import type { Definition, Question, SimpleBlock } from "~/composables/types"
import { useDefinitionStore } from "~/stores/definitionStore"
import { useQuestionnaireStore } from "~/stores/questionnaireStore"

export const useQuestionHandler = (question: Question) => {
  const questionnaireStore = useQuestionnaireStore()
  const definitionStore = useDefinitionStore()

  const criteria = computed(() => {
    return questionnaireStore.criteriaById[question.criteriaId!]
  })
  const definitions = computed<{ [key: number]: Definition }>(() =>
    criteria.value?.definitionIds.length > 0
      ? definitionStore.definitionsByIdArray(criteria.value.definitionIds)
      : [],
  )
  const explanatory = computed<SimpleBlock[]>(
    () =>
      criteria.value?.explanatory.map(
        (item: { value: SimpleBlock[] }) => item.value,
      ) || [],
  )
  return {
    criteria,
    definitions,
    explanatory,
  }
}
