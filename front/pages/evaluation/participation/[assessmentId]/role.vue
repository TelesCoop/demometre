<template>
  <div class="container is-tight">
    <h1 class="title is-3 mt-2 has-text-black">
      {{ pageStore.evaluationQuestionnairePage.roleQuestionTitle }}
    </h1>
    <RichText
      v-if="pageStore.evaluationQuestionnairePage.roleQuestionDescription"
      class="is-family-secondary"
      :rich-text="pageStore.evaluationQuestionnairePage.roleQuestionDescription"
    />

    <ButtonsArrowButton
      color="no-pillar"
      class="arrow-button-fixed is-left"
      @click.prevent="goBack"
    />

    <FormRole
      v-model="answer"
      :is-loading="isLoading"
      @submit="onSubmit"
    />
  </div>
</template>

<script setup lang="ts">
import { useParticipationStore } from "~/stores/participationStore"
import { useProfilingJourney } from "~/composables/journey"
import { usePageStore } from "~/stores/pageStore"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { useAssessmentIsReady } from "~/composables/useAssessmentIsReady"

definePageMeta({
  title: "Question sur le role",
  step: "role",
})

await useAssessmentIsReady()

const assessmentStore = useAssessmentStore()
const router = useRouter()
const participationStore = useParticipationStore()
const pageStore = usePageStore()
if (!pageStore.evaluationQuestionnairePage.startTitle) {
  pageStore.getEvaluationQuestionnairePage()
}

const answer = ref(participationStore.newParticipation.roleId)
const isLoading = ref(false)

function goBack() {
  router.push(
    `/evaluation/participation/${assessmentStore.currentAssessmentId}/tableau-de-bord`,
  )
}

async function onSubmit() {
  isLoading.value = true
  participationStore.chooseRole(answer.value)
  const isSuccess = await participationStore.createParticipation()

  if (isSuccess) {
    await participationStore.getQuestionnaireObjectiveQuestionResponsesForAssessment(
      assessmentStore.currentAssessmentId,
    )
    const journey = useProfilingJourney()
    journey.goToNextQuestion(undefined)
  }
}
</script>
