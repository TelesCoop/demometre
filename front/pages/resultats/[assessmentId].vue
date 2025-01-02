<template>
  <div>
    <div class="container">
      <PageTitle
        :title="assessmentStore.assessmentById[assessmentId]?.name"
        class="mt-4"
      />
    </div>

    <div class="container mobile-mode mb-4">
      <section class="section">
        <div class="is-flex is-justify-content-space-between">
          <h2 class="title is-3 has-text-shade-700 mb-1">
            {{ $t("Résultats par piliers") }}
          </h2>
          <nuxt-link
            class="button is-rounded is-responsive is-shade-600"
            to="/demometre"
          >
            <span>{{ $t("En savoir plus sur le DémoMètre") }}</span>
            <span class="icon">
              <icon
                size="20"
                name="arrow-right-line"
              />
            </span>
          </nuxt-link>
        </div>
        <div class="columns is-multiline mt-4">
          <div
            v-for="pillar of pillars"
            :key="pillar.name"
            class="column"
          >
            <QuestionnairePillar
              :name="pillar.name"
              :active="pillar.name === activePillar?.name"
              :score="
                getScoreToDisplay(
                  assessmentStore.scoresByAssessmentId[assessmentId]
                    ?.byPillarId[pillar.id],
                )
              "
              class="is-clickable"
              @click="onSelectPillar(pillar, true)"
            />
          </div>
        </div>
      </section>
      <section v-if="activePillar">
        <QuestionnairePillarReferential
          :pillar="activePillar"
          :color="colorClass"
          :markers="markers"
          :initial-question-id="activeQuestionId"
          :show-scores="true"
          :scores="assessmentStore.scoresByAssessmentId[assessmentId]"
        >
          <template #criteria="criteriaProps">
            <RichText
              v-if="criteriaProps.criteria.description"
              :rich-text="criteriaProps.criteria.description"
              class="is-family-secondary subtitle mb-2"
            />
            <QuestionnaireQuestionStatement
              v-for="questionId of criteriaProps.criteria.questionIds"
              :key="questionId"
              :color="colorClass"
              :question="questionnaireStore.questionById[questionId]"
              class="mb-4"
              data-cy="question-result"
            >
              <div
                v-if="
                  questionnaireStore.questionById[questionId]
                    .explainsByQuestionIds.length
                "
              >
                <p class="is-uppercase is-size-6bis mb-0_5 mt-1">
                  {{ $t("Explicitée par :") }}
                </p>
                <a
                  v-for="explainsByQuestionId of questionnaireStore
                    .questionById[questionId].explainsByQuestionIds"
                  :key="explainsByQuestionId"
                  class="is-underlined"
                  @click="onSelectQuestion(explainsByQuestionId)"
                >
                  <span>
                    {{
                      questionnaireStore.questionById[explainsByQuestionId]
                        ?.name
                    }}
                  </span>
                </a>
              </div>
              <div
                v-if="
                  questionnaireStore.questionById[questionId].allowsToExplain
                "
              >
                <p class="is-uppercase is-size-6bis mb-0_5 mt-1">
                  {{ $t("Permet d'expliciter :") }}
                </p>
                <a
                  class="is-underlined"
                  @click="
                    onSelectQuestion(
                      questionnaireStore.questionById[questionId]
                        .allowsToExplain,
                    )
                  "
                >
                  <span>
                    {{
                      questionnaireStore.questionById[
                        questionnaireStore.questionById[questionId]
                          .allowsToExplain
                      ]?.name
                    }}
                  </span>
                </a>
              </div>
              <p class="is-uppercase is-size-6bis mb-0_5 mt-2">
                {{ $t("Résultat") }}
              </p>
              <AnalyticsChartByQuestionType
                :color="colorClass"
                :assessment-id="assessmentId"
                :question="questionnaireStore.questionById[questionId]"
              />
            </QuestionnaireQuestionStatement>
          </template>
          <template #marker="markerProps">
            <RichText
              v-if="markerProps.marker.description"
              :rich-text="markerProps.marker.description"
              class="is-family-secondary subtitle mb-2"
            />
            <AnalyticsPlusAndMinus
              :strengths-and-improvements="
                getStrenghtAndImprovements(
                  assessmentStore.scoresByAssessmentId[assessmentId],
                  markerProps.marker.criteriaIds,
                  'marker',
                )
              "
            />
          </template>
          <template #pillar="pillarProps">
            <AnalyticsPlusAndMinus
              :strengths-and-improvements="
                getStrenghtAndImprovements(
                  assessmentStore.scoresByAssessmentId[assessmentId],
                  pillarProps.pillar.markerIds,
                  'pillar',
                )
              "
            />
          </template>
        </QuestionnairePillarReferential>
      </section>
    </div>

    <div class="container">
      <ParticipationBoard
        :assessment="assessmentStore.assessmentById[assessmentId]"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"
import { Ref, ref } from "vue"
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { Marker, PillarType } from "~/composables/types"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { getStrenghtAndImprovements, getScoreToDisplay } from "~/utils/scores"
import { useAssessmentIsReady } from "~/composables/useAssessmentIsReady"

definePageMeta({
  title: "Résultats",
  breadcrumb: "Résultats",
})

const router = useRouter()

const assessmentStore = useAssessmentStore()
const route = useRoute()
const assessmentIdStr: string = (route.params.assessmentId as string)
const assessmentId = parseInt(assessmentIdStr as string)
await useAssessmentIsReady()

const questionnaireStore = useQuestionnaireStore()

const activePillar = ref<PillarType>()
const markers = ref<Marker[]>()

const changeSelectedQuestion = ref<number>(0)
const activeQuestionId: Ref<number> = ref(
  parseInt(route.query.question as string),
)
const pillars = computed(() => {
  return questionnaireStore.surveyById[
    assessmentStore.currentAssessment.surveyId
  ].pillars
})

if (!assessmentStore.assessmentById[assessmentId]?.name) {
  assessmentStore.getAssessment(assessmentId)
}
if (!assessmentStore.scoresByAssessmentId[assessmentId]) {
  assessmentStore.getAssessmentScores(assessmentId)
}

const pillarOfQuestionId = (questionId: number) => {
  return questionnaireStore.pillarById[
    questionnaireStore.questionById[questionId].pillarId
  ]
}
const changeActiveQuestionId = () => {
  if (activeQuestionId.value) {
    const pillar = pillarOfQuestionId(activeQuestionId.value)
    onSelectPillar(pillar)
  }
}

watch(
  () => route.query.question,
  () => {
    activeQuestionId.value = parseInt(route.query.question as string)
    changeActiveQuestionId()
  },
)
watch(changeSelectedQuestion, () => {
  changeActiveQuestionId()
})

const colorClass = computed(() =>
  activePillar.value ? PillarParams[activePillar.value.name].color : "",
)

const onSelectPillar = (pillar, cleanUrl = false) => {
  activePillar.value = pillar
  markers.value = activePillar.value?.markerIds.map(
    (markerId) => questionnaireStore.markerById[markerId],
  )
  const query = cleanUrl
    ? { pillar: pillar.name }
    : { ...route.query, pillar: pillar.name }
  router.push({ query })
}

const onSelectQuestion = (questionId) => {
  changeSelectedQuestion.value += 1
  activeQuestionId.value = questionId
  router.replace({ query: { ...route.query, question: questionId } })
}

changeActiveQuestionId()
</script>

<style scoped lang="sass"></style>
