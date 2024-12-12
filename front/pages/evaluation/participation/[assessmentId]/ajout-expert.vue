<template>
  <div>
    <PageSection
      class="column is-8 questionnaire-container"
      :title="
        pageStore.evaluationInitiationPage.createAssessmentWithExpertTitle
      "
      :intro="
        pageStore.evaluationInitiationPage.createAssessmentWithExpertDescription
      "
      :is-first-element="true"
      :intro-is-rich-text="true"
    >
      <div class="nav-questionnaire-container">
        <div v-if="!userStore.isLoggedIn">
          <!-- User not logged in -->
          <p class="mb-1">
            {{ $t("Vous devez être connecté pour ajouter un expert") }}
          </p>
          <div class="buttons mb-0_5">
            <NuxtLink
              class="button is-shade-600 is-rounded"
              to="/signup"
            >
              {{ $t("Créer un compte") }}
            </NuxtLink>
            <NuxtLink
              class="button is-shade-600 is-rounded"
              to="/login"
            >
              {{ $t("Se connecter") }}
            </NuxtLink>
          </div>
        </div>
        <AssessmentAddExpert
          v-else
          v-model="expertSelected"
          :initiation-page="pageStore.evaluationInitiationPage"
        />
        <ButtonsArrowButton
          color="no-pillar"
          class="arrow-button-fixed is-left"
          @click.prevent="goBack"
        />
        <button
          class="button is-shade-600 is-rounded mt-4"
          :disabled="disabled"
          @click.prevent="onSubmit"
        >
          <span>{{ $t("C’est parti !") }}</span>
        </button>
      </div>
    </PageSection>
  </div>
</template>

<script setup lang="ts">
import { usePageStore } from "~/stores/pageStore"
import { useUserStore } from "~/stores/userStore"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { User } from "~/composables/types"
import { useAssessmentIsReady } from "~/composables/useAssessmentIsReady"

definePageMeta({
  title: "Ajout d'un expert",
  breadcrumb: "Ajout d'un expert",
  step: "participation",
})

const assessmentStore = useAssessmentStore()
await useAssessmentIsReady()

const router = useRouter()

const disabled = computed(() =>
  !assessmentStore.newAssessment.conditionsOfSaleConsent,
)

const userStore = useUserStore()
const pageStore = usePageStore()
if (!pageStore.evaluationInitiationPage.initTitle) {
  pageStore.getEvaluationInitiationPage()
}

const expertSelected = ref<User>()

function goBack() {
  router.push(
    `/evaluation/participation/${assessmentStore.currentAssessmentId}`,
  )
}

async function onSubmit() {
  const isSuccess = await assessmentStore.addExpert(
    +route.params.assessmentId,
    expertSelected.value.id,
  )
  if (isSuccess) {
    assessmentStore.addingExpert = false
    useRouter().push(
      `/evaluation/participation/${assessmentStore.currentAssessmentId}/tableau-de-bord`,
    )
  }
}
</script>
