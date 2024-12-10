<template>
  <div class="container">
    <section class="columns is-desktop section">
      <div class="column is-5-desktop">
        <PageTitle
          v-if="pillarsCompleted.length - pillarsWithoutQuestions.length === 0"
          :title="pageStore.evaluationQuestionnairePage.startTitle"
          :subtitle="pageStore.evaluationQuestionnairePage.startText"
        />
        <PageTitle
          v-else-if="pillarsCompleted.length === 4"
          :title="pageStore.evaluationQuestionnairePage.finishedTitle"
          :subtitle="
            userStore.isLoggedIn
              ? pageStore.evaluationQuestionnairePage.finishedTextLoggedIn
              : pageStore.evaluationQuestionnairePage.finishedTextLoggedOut
          "
        />
        <PageTitle
          v-else
          :title="intermediateStepTitle"
          :subtitle="
            userStore.isLoggedIn
              ? pageStore.evaluationQuestionnairePage
                .intermediateStepTextLoggedIn
              : pageStore.evaluationQuestionnairePage
                .intermediateStepTextLoggedOut
          "
        />
        <div class="buttons">
          <button
            v-if="userStore.isUnknownUser"
            class="button is-normal is-rounded is-outlined is-responsive is-shade-600"
            @click="participationStore.setShowSaveParticipationModal(true)"
          >
            <span>{{ $t("Enregistrer") }}</span>
            <span class="icon">
              <icon
                size="20"
                name="save"
              />
            </span>
          </button>
          <nuxt-link
            v-if="pillarsCompleted.length === 4"
            class="button is-normal is-rounded is-outlined is-responsive is-shade-600"
            to="/resultats"
          >
            <span>{{ $t("Voir les résultats") }}</span>
            <span class="icon">
              <icon
                size="20"
                name="bar-chart-box-line"
              />
            </span>
          </nuxt-link>
        </div>
      </div>

      <div class="column is-6-desktop is-offset-1">
        <!-- Pillar navigation for desktop  -->
        <QuestionnaireRosette
          class="rosette-menu"
          :center-button-name="rosetteButtonText"
          :pillars-completed="pillarsCompleted"
          @center-button-click="onStartQuestionnaire"
          @pillar-click="onRosettePillarClicked($event)"
          @marker-click="onRosetteMarkerClicked($event)"
        />
        <!-- Pillar navigation for mobile  -->
        <section
          ref="pillarsRef"
          class="columns is-multiline mt-4 list-menu"
        >
          <div
            v-for="pillar of questionnaireStore.pillarsOfSurvey(
              assessment?.surveyId,
            )"
            :key="pillar.name"
            class="column"
          >
            <QuestionnairePillar
              :name="pillar.name"
              :is-completed="pillarsCompleted.includes(pillar.name)"
              style="cursor: pointer"
              @click="onRosettePillarClicked(pillar.name)"
            />
          </div>
        </section>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useQuestionnaireJourney } from "~/composables/journey"
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { usePageStore } from "~/stores/pageStore"
import { useParticipationStore } from "~/stores/participationStore"
import { useUserStore } from "~/stores/userStore"
import { useAssessmentStore } from "~/stores/assessmentStore"

definePageMeta({
  title: "Questionnaire",
  step: "questionnaire",
})

const assessmentStore = useAssessmentStore()
const questionnaireStore = useQuestionnaireStore()
const participationStore = useParticipationStore()
const pageStore = usePageStore()
const userStore = useUserStore()

const assessment = assessmentStore.currentAssessment

if (
  Object.keys(participationStore.totalAndAnsweredQuestionsByPillarName)
    .length !== 4
) {
  participationStore.setTotalAndAnsweredQuestionsByPillarName()
}

if (!pageStore.evaluationQuestionnairePage.startTitle) {
  pageStore.getEvaluationQuestionnairePage()
}
const rosetteButtonText = computed(() => {
  const total = Object.values(
    participationStore.totalAndAnsweredQuestionsByPillarName,
  ).reduce(
    (accum: any, total: any) => {
      accum.completed += total.completed ? 1 : 0
      accum.hasStarted = accum.hasStarted || total.answered > 0
      return accum
    },
    { completed: 0, hasStarted: false },
  )

  if (total.completed === 4) {
    return ""
  }
  return total.hasStarted ? $t("Continuer") : $t("Commencer")
})

const pillarsCompleted = computed(() =>
  Object.keys(participationStore.totalAndAnsweredQuestionsByPillarName).filter(
    (pillarName) =>
      participationStore.totalAndAnsweredQuestionsByPillarName[pillarName]
        .completed,
  ),
)
const pillarsWithoutQuestions = computed(() =>
  Object.keys(participationStore.totalAndAnsweredQuestionsByPillarName).filter(
    (pillarName) =>
      participationStore.totalAndAnsweredQuestionsByPillarName[pillarName]
        .completed &&
      participationStore.totalAndAnsweredQuestionsByPillarName[pillarName]
        .answered === 0,
  ),
)

const intermediateStepTitle = computed(() => {
  const pillarNames = pageStore.evaluationQuestionnairePage
    .isIntermediateStepTitleWithPillarNames
    ? pillarsCompleted.value.join(", ")
    : ""
  return `${pageStore.evaluationQuestionnairePage.intermediateStepTitle} ${pillarNames}`
})

const startPillar = (pillarName: string) => {
  const { lastQuestionId, isLast } = getLastQuestionOfPillar(pillarName)
  const journey = useQuestionnaireJourney(pillarName)
  journey.goToNextQuestion(isLast ? undefined : lastQuestionId)
}

const onStartQuestionnaire = () => {
  const pillarsOfSurvey = questionnaireStore.pillarsOfSurvey(
    assessment?.surveyId,
  )
  const pillar =
    pillarsOfSurvey.find(
      (pillar) => !pillarsCompleted.value.includes(pillar.name),
    ) || pillarsOfSurvey[0]

  const pillarName = questionnaireStore.pillarById[pillar?.id].name
  startPillar(pillarName)
}
const onRosettePillarClicked = (pillarName) => {
  startPillar(pillarName)
}
const onRosetteMarkerClicked = (markerId) => {
  onRosettePillarClicked(questionnaireStore.markerById[markerId].pillarName)
}
</script>

<style scoped lang="sass">
.buttons .button
  height: fit-content

.list-menu
  display: none

@include mobile
  .rosette-menu
    display: none
  .list-menu
    display: block
</style>
