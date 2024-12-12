<template>
  <PageSection
    :title="pageStore.evaluationInitiationPage.objectiveQuestionsTitle"
    :intro="pageStore.evaluationInitiationPage.objectiveQuestionsDescription"
    :is-first-element="true"
    :intro-is-rich-text="true"
    class="column is-8 questionnaire-container"
  >
    <div class="nav-questionnaire-container">
      <button
        class="button is-shade-600 is-rounded mt-4"
        @click.prevent="goToFirstObjectiveQuestion"
      >
        <span>{{
          pageStore.evaluationInitiationPage.objectiveQuestionsCallToAction
        }}</span>
        <span class="icon">
          <icon
            v-if="isLoading"
            size="20"
            name="loader-2-line"
          />
          <icon
            v-else
            size="20"
            name="arrow-right-line"
          />
        </span>
      </button>
      <span
        v-if="isLoading"
        class="is-size-7 has-text-shade-600"
      >{{ $t("en cours de chargement") }}</span>
      <!-- <ButtonsArrowButton class="arrow-button-fixed is-left" @click.prevent="goBack" color="no-pillar" /> -->
    </div>
  </PageSection>
</template>

<script setup lang="ts">
import { useInitializationJourney } from "~/composables/journey"
import { usePageStore } from "~/stores/pageStore"
import { useI18n } from "vue-i18n"
import { useAssessmentIsReady } from "~/composables/useAssessmentIsReady"

const i18n = useI18n()
const $t = i18n.t

definePageMeta({
  // title: $t("Initialisation"),
  step: "initialization-objectives-questions",
})

await useAssessmentIsReady()

const pageStore = usePageStore()
if (!pageStore.evaluationInitiationPage.objectiveQuestionsTitle) {
  pageStore.getEvaluationInitiationPage()
}

const isLoading = ref(false)

const goToFirstObjectiveQuestion = () => {
  isLoading.value = true
  const journey = useInitializationJourney()
  journey.goToNextQuestion(undefined)
}
</script>
