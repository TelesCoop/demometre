<template>
  <PageSection
    class="column is-8"
    :title="pageStore.evaluationInitiationPage.searchAssessmentTitle"
    :intro="pageStore.evaluationInitiationPage.searchAssessmentDescription"
    :is-first-element="true"
  >
    <FormLocalisation
      :label="
        pageStore.evaluationInitiationPage.searchAssessmentLocalityTypeQuestion
      "
      :description="
        pageStore.evaluationInitiationPage
          .searchAssessmentLocalityTypeDescription
      "
      @submit="onSubmit"
    />
  </PageSection>
</template>

<script setup lang="ts">
import { useAssessmentStore } from "~/stores/assessmentStore"
import { LocalityTypes } from "~/composables/types"
import { usePageStore } from "~/stores/pageStore"

definePageMeta({
  title: "Localisation",
  step: "localisation",
})
const router = useRouter()
const assessmentStore = useAssessmentStore()
const pageStore = usePageStore()

if (!pageStore.evaluationInitiationPage.searchAssessmentTitle) {
  pageStore.getEvaluationInitiationPage()
}
async function onSubmit(data: {
  localityId: number
  localityType: LocalityTypes
}) {
  const isSuccess = await assessmentStore.getOrCreateAssessment(data)
  if (isSuccess) {
    if (!assessmentStore.currentAssessment?.initializationDate) {
      router.push(
        `/evaluation/initialisation?assessment=${assessmentStore.currentAssessmentId}`,
      )
    } else {
      router.push(
        `/evaluation/participation/${assessmentStore.currentAssessmentId}`,
      )
    }
  }
}
</script>
