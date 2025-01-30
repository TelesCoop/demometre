<template>
  <div>
    <!-- Choose Assessment type step-->
    <PageSection
      v-if="initializationSteps[currentStep] === steps.ASSESSMENT_TYPE"
      :title="pageStore.evaluationInitiationPage.noAssessmentTitle"
      :intro="pageStore.evaluationInitiationPage.noAssessmentDescription"
      :is-first-element="true"
      :intro-is-rich-text="true"
      class="questionnaire-container column is-10"
    >
      <div class="columns mb-2 nav-questionnaire-container">
        <div
          v-for="assessmentType in pageStore.usagePage.startAssessmentBlockData"
          :key="assessmentType.id"
          class="column is-one-third"
        >
          <PageAssessmentCard
            :assessment-type="assessmentType"
            background-color="white"
          />
        </div>
        <ButtonsArrowButton
          color="no-pillar"
          class="arrow-button-fixed is-left"
          @click.prevent="goBack"
        />
      </div>
    </PageSection>

    <!-- User not logged in can not initialize assessment-->
    <PageSection
      v-else-if="!userStore.isLoggedIn"
      class="column is-8"
      :title="pageStore.evaluationInitiationPage.mustBeConnectedToCreateTitle"
      :intro="
        pageStore.evaluationInitiationPage.mustBeConnectedToCreateDescription
      "
      :is-first-element="true"
    >
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
    </PageSection>

    <!-- Start initialization step -->
    <PageSection
      v-else-if="initializationSteps[currentStep] === steps.START"
      class="column is-8 questionnaire-container"
      :title="startInitializationTitleAndDesc[0]"
      :intro="startInitializationTitleAndDesc[1]"
      :is-first-element="true"
      :intro-is-rich-text="true"
    >
      <div class="nav-questionnaire-container">
        <div
          v-if="
            assessmentStore.newAssessment.assessmentType ===
              AssessmentType.WITH_EXPERT.key
          "
        >
          <AssessmentAddExpert
            v-model="expertSelected"
            :initiation-page="pageStore.evaluationInitiationPage"
          />
        </div>
        <ParticipationConsent
          class="mt-1_5"
          type="cgu"
          :initiator="true"
        />
        <ButtonsArrowButton
          color="no-pillar"
          class="arrow-button-fixed is-left"
          type="button"
          @click.prevent="goBack"
        />
        <button
          class="button is-shade-600 is-rounded mt-4"
          :disabled="disabled"
          type="button"
          data-cy="consent-submit"
          @click.prevent="goToNextStep"
        >
          <span>{{ $t("Valider") }}</span>
        </button>
      </div>
    </PageSection>

    <!-- Assessment Initiator step -->
    <PageSection
      v-else-if="initializationSteps[currentStep] === steps.INITIATOR"
      class="column is-8 questionnaire-container"
      :title="pageStore.evaluationInitiationPage.initTitle"
      :intro="pageStore.evaluationInitiationPage.initDescription"
      :is-first-element="true"
      :intro-is-rich-text="true"
    >
      <form
        class="nav-questionnaire-container"
        @submit.prevent="goToNextStep"
      >
        <div class="field mb-2">
          <label class="label">{{
            pageStore.evaluationInitiationPage.initiatorNameQuestion
          }}</label>
          <span class="is-family-secondary is-size-6">{{
            pageStore.evaluationInitiationPage.initiatorNameDescription
          }}</span>
          <div class="control mt-0_5">
            <input
              v-model="initiatorName"
              class="input is-normal-width"
              type="text"
              data-cy="initiator-name"
              placeholder="Mairie de ..."
            >
          </div>
        </div>
        <label class="label">{{ $t("Au nom de qui lancez-vous cette évaluation ?") }}</label>
        <div class="buttons mt-1">
          <div
            v-for="initiatorType of InitiatorType"
            :key="initiatorType.key"
            class="margin-between"
          >
            <input
              :id="initiatorType.key"
              v-model="initiatorTypeSelected"
              type="radio"
              :value="initiatorType.key"
              class="custom-hidden white-on-black-input-checked"
              name="initiationType"
              required
            >
            <label
              :for="initiatorType.key"
              :data-cy="`initiator-type-${initiatorType.key}`"
              class="button is-shade-600 is-outlined locality"
            >{{ initiatorType.value }}</label>
          </div>
        </div>
        <div class="buttons mt-4">
          <button
            class="button is-shade-600 is-rounded"
            :disabled="disabled"
            data-cy="initiator-submit"
          >
            <span>{{ $t("Valider") }}</span>
            <span class="icon">
              <icon
                size="20"
                name="check"
              />
            </span>
          </button>

          <!-- Permet d'appuyer sur entrer -->
          <input
            type="submit"
            hidden
          >
        </div>

        <ButtonsArrowButton
          color="no-pillar"
          class="arrow-button-fixed is-left"
          @click.prevent="goBack"
        />
      </form>
    </PageSection>

    <!-- Representativity rates step -->
    <PageSection
      v-else-if="initializationSteps[currentStep] === steps.REPRESENTATIVITY"
      class="column is-8 questionnaire-container"
      :title="pageStore.evaluationInitiationPage.representativityTitle"
      :intro="pageStore.evaluationInitiationPage.representativityDescription"
      :is-first-element="true"
      :intro-is-rich-text="true"
    >
      <form
        class="nav-questionnaire-container"
        @submit.prevent="onSubmit"
      >
        <div
          v-for="representativityCriteria of assessmentStore.representativityCriteriasForSurveyLocality(
            assessmentStore.currentAssessment.surveyLocality,
          )"
          :key="representativityCriteria.id"
        >
          <label class="label is-size-5">{{
            representativityCriteria.name
          }}</label>
          <RichText
            class="is-family-secondary is-size-6"
            :rich-text="representativityCriteria.explanation"
          />
          <ResponseInputPercentage
            v-model="representativityCriteria.acceptabilityThreshold"
            class="mt-1"
            :color="color"
            :question-id="representativityCriteria.id"
          />
        </div>
        <div class="buttons mt-1_5">
          <button
            class="button is-shade-600 is-rounded"
            :disabled="disabled"
          >
            <span>{{ $t("Valider") }}</span>
            <span class="icon">
              <icon
                size="20"
                name="check"
              />
            </span>
          </button>

          <!-- Permet d'appuyer sur entrer -->
          <input
            type="submit"
            hidden
          >
        </div>

        <ButtonsArrowButton
          color="no-pillar"
          class="arrow-button-fixed is-left"
          @click.prevent="goBack"
        />
      </form>
    </PageSection>
  </div>
</template>

<script setup lang="ts">
import { usePageStore } from "~/stores/pageStore"
import { InitiatorType, AssessmentType } from "~/composables/types"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { useUserStore } from "~/stores/userStore"
import { useAssessmentIsReady } from "~/composables/useAssessmentIsReady"

definePageMeta({
  title: "Initialisation",
  step: "initialization",
})

await useAssessmentIsReady()

const router = useRouter()
const userStore = useUserStore()

const pageStore = usePageStore()
if (!pageStore.evaluationInitiationPage.initTitle) {
  pageStore.getEvaluationInitiationPage()
}
if (!pageStore.usagePage.startAssessmentBlockData) {
  pageStore.getUsagePage()
}

const assessmentStore = useAssessmentStore()
if (assessmentStore.representativityCriterias.length === 0) {
  assessmentStore.getRepresentativityCriterias()
}

const expertSelected = ref<User>()

const color = ref("no-pillar")

enum steps {
  ASSESSMENT_TYPE = "assessment_type",
  START = "start",
  INITIATOR = "initiator",
  REPRESENTATIVITY = "representativity",
}

const initializationSteps = [
  steps.ASSESSMENT_TYPE,
  steps.START,
  steps.INITIATOR,
  // At the last moment it was decided not to give the possibility to customize the representativity in order not to confuse the user
  // steps.REPRESENTATIVITY,
]
const currentStep = ref<number>(
  assessmentStore.newAssessment.assessmentType ? 1 : 0,
)

const initiatorTypeSelected = ref<string>()
const initiatorName = ref<string>("")

watch(
  () => assessmentStore.newAssessment.assessmentType,
  () => {
    if (
      currentStep.value === 0 &&
      assessmentStore.newAssessment.assessmentType
    ) {
      currentStep.value = 1
    }
  },
)

const disabled = computed(() => {
  switch (initializationSteps[currentStep.value]) {
    case steps.START: {
      const cguConsent = assessmentStore.newAssessment.initiatorUsageConsent
      const cgvConsent =
        assessmentStore.newAssessment.assessmentType ===
        AssessmentType.WITH_EXPERT.key
          ? assessmentStore.newAssessment.conditionsOfSaleConsent
          : true
      return !(cguConsent && cgvConsent)
    }
    case steps.INITIATOR:
      return !(initiatorTypeSelected.value && initiatorName.value)
    default:
      return false
  }
})

const startInitializationTitleAndDesc = computed(() => {
  switch (assessmentStore.newAssessment.assessmentType) {
    case AssessmentType.QUICK.key:
      return [
        pageStore.evaluationInitiationPage.createQuickAssessmentTitle,
        pageStore.evaluationInitiationPage.createQuickAssessmentDescription,
      ]
    case AssessmentType.PARTICIPATIVE.key:
      return [
        pageStore.evaluationInitiationPage.createParticipationAssessmentTitle,
        pageStore.evaluationInitiationPage
          .createParticipationAssessmentDescription,
      ]
    case AssessmentType.WITH_EXPERT.key:
      return [
        pageStore.evaluationInitiationPage.createAssessmentWithExpertTitle,
        pageStore.evaluationInitiationPage
          .createAssessmentWithExpertDescription,
      ]
  }
})

onMounted(() => {
  window.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      goToNextStep()
    }
  })
})

function goBack() {
  if (initializationSteps[currentStep.value] === steps.ASSESSMENT_TYPE) {
    assessmentStore.currentAssessmentId = undefined
    router.push("/evaluation/localisation")
  } else if (initializationSteps[currentStep.value] === steps.START) {
    assessmentStore.newAssessment.assessmentType = undefined
    currentStep.value -= 1
  } else {
    currentStep.value -= 1
  }
}

function goToNextStep() {
  if (disabled.value) {
    return
  }
  if (initializationSteps.length - 1 > currentStep.value) {
    if (
      initializationSteps[currentStep.value + 1] === steps.REPRESENTATIVITY &&
      assessmentStore.newAssessment.assessmentType === AssessmentType.QUICK.key
    ) {
      // There is no representativity logic for quick diagnostics
      onSubmit()
    } else {
      currentStep.value += 1
    }
  } else {
    onSubmit()
  }
}

async function onSubmit() {
  const isSuccess = await assessmentStore.initializeAssessment({
    initiatorType: initiatorTypeSelected.value,
    initiatorName: initiatorName.value,
    expertId: expertSelected.value?.id || null,
  })
  if (isSuccess) {
    useRouter().push(
      `/evaluation/initialisation/${assessmentStore.currentAssessmentId}/questions-objectives`,
    )
  }
}
</script>
