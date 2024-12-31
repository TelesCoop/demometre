<template>
  <div class="container">
    <section class="section columns is-centered questionnaire-container">
      <div class="column is-8 nav-questionnaire-container">
        <h1 class="title is-3 has-text-black-ter">
          {{ pageStore.evaluationQuestionnairePage.endOfProfilingTitle }}
        </h1>
        <RichText
          :rich-text="
            pageStore.evaluationQuestionnairePage.endOfProfilingDescription
          "
          class="is-family-secondary"
        />

        <ButtonsArrowButton
          class="arrow-button-fixed is-left"
          color="no-pillar"
          @click.prevent="goBack"
        />

        <button
          class="button is-shade-600 is-rounded mt-4"
          data-cy="affinage-continue"
          @click.prevent="submit"
        >
          <span>{{
            pageStore.evaluationQuestionnairePage.endOfProfilingCallToAction
          }}</span>
          <span class="icon">
            <icon
              size="16"
              name="check"
            />
          </span>
        </button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { usePageStore } from "~/stores/pageStore"
import { useParticipationStore } from "~/stores/participationStore"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { useAssessmentIsReady } from "~/composables/useAssessmentIsReady"

definePageMeta({
  title: "Affinage",
  step: "profiling",
})

await useAssessmentIsReady()

const router = useRouter()
const participationStore = useParticipationStore()
const assessmentStore = useAssessmentStore()
const pageStore = usePageStore()
if (!pageStore.evaluationQuestionnairePage.endOfProfilingTitle) {
  pageStore.getEvaluationQuestionnairePage()
}

function goBack() {
  router.go(-1)
}

async function submit() {
  await participationStore.saveEndQuestionnaire(true)
  useRouter().push(`/evaluation/${assessmentStore.currentAssessmentId}/questionnaire`)
}
</script>
