<template>
  <Suspense>
    <template #default>
      <div class="container is-tight">
        <Question
          v-if="context"
          :context="context"
          :question-id="questionId"
          :is-questionnaire="true"
          :color="color"
        />
      </div>
    </template>
    <template #fallback>
      <p>...</p>
    </template>
  </Suspense>
</template>

<script setup lang="ts">
import { useQuestionnaireJourney } from "~/composables/journey"
import { useParticipationStore } from "~/stores/participationStore"
import { QuestionContextProps, PillarParams } from "~/composables/types"
import { Ref, ref } from "vue"
import { useQuestionnaireStore } from "~/stores/questionnaireStore"

definePageMeta({
  title: "Questionnaire",
  step: "questionnaire",
})

const route = useRoute()
const router = useRouter()
const questionnaireStore = useQuestionnaireStore()
const participationStore = useParticipationStore()

const questionId: Ref<number> = ref(+route.params.questionId)
let pillarName = questionnaireStore.questionById[questionId.value].pillarName!
let journey = useQuestionnaireJourney(pillarName)
const color = computed<string>(() => PillarParams[pillarName].color)

router.beforeEach(async (to) => {
  // This function is call each time the url change and this page is loaded in the client side
  if (
    +to.params.questionId &&
    route.path.includes("evaluation/questionnaire")
  ) {
    questionId.value = +to.params.questionId
    pillarName = questionnaireStore.questionById[questionId.value].pillarName!
    journey = useQuestionnaireJourney(pillarName)
  }
})

const context: QuestionContextProps = {
  journey,
  questionById: questionnaireStore.questionById,
  responseByQuestionId: participationStore.responseByQuestionnaireQuestionId,
  hasPreviousStep: true,
}
</script>
