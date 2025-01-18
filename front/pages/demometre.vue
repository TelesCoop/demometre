<template>
  <div>
    <div class="container">
      <section class="columns section is-desktop">
        <div class="column is-6-desktop">
          <div class="pb-2">
            <PageTitle
              :title="pageStore.referentialPage.title"
              :subtitle="pageStore.referentialPage.introduction"
              :margin-bottom="1"
            />
            <RichText
              :rich-text="pageStore.referentialPage.description"
              class="is-family-secondary"
            />
          </div>
          <div class="buttons are-normal is-shade-600">
            <!--Hash url does not work with ssr mode -->
            <nuxt-link
              class="button is-dark is-rounded is-responsive is-outlined is-shade-600"
              to="/projet?hash=howBlockRef"
            >
              <span>{{ $t("Comment on a construit le référentiel") }}</span>

              <span class="icon">
                <icon name="arrow-right-line" size="20" />
              </span>
            </nuxt-link>
          </div>
        </div>
        <div class="column is-5-desktop is-offset-1">
          <QuestionnaireRosette
            class="rosette-menu"
            :center-button-name="$t('Découvrir')"
            @center-button-click="onDiscoverButtonClick()"
            @pillar-click="onRosettePillarClicked($event)"
            @marker-click="onRosetteMarkerClicked($event)"
          />
          <RichText
            :rich-text="pageStore.referentialPage.rosetteLegend"
            class="rosette-legend mt-1"
          />
        </div>
      </section>
    </div>

    <div ref="explicationRef" class="has-background-shade-100 scroll">
      <PageSection
        v-if="pageStore.referentialPage.pillarBlockTitle"
        :title="pageStore.referentialPage.pillarBlockTitle"
      >
        <div class="columns is-variable is-8">
          <RichText
            :rich-text="pageStore.referentialPage.pillarBlockLeftContent"
            class="is-family-secondary column"
          />
          <div class="column">
            <RichText
              :rich-text="pageStore.referentialPage.pillarBlockRightContent"
              class="is-family-secondary"
            />
            <img
              v-if="pageStore.referentialPage.pillarBlockImageUrl"
              :src="
                MEDIA_BASE_URL + pageStore.referentialPage.pillarBlockImageUrl
              "
              alt="image des piliers"
              :style="`max-height: 250px`"
            >
          </div>
        </div>
      </PageSection>
      <PageSection
        v-if="pageStore.referentialPage.markerBlockTitle"
        :title="pageStore.referentialPage.markerBlockTitle"
      >
        <div class="columns is-align-items-center">
          <RichText
            :rich-text="pageStore.referentialPage.markerBlockContent"
            class="is-family-secondary column"
          />
          <QuestionnaireRosetteCooperation class="column" />
        </div>
      </PageSection>

      <PageSection
        v-if="pageStore.referentialPage.criteriaBlockTitle"
        :title="pageStore.referentialPage.criteriaBlockTitle"
      >
        <div class="columns is-variable is-8">
          <RichText
            :rich-text="pageStore.referentialPage.criteriaBlockLeftContent"
            class="is-family-secondary column"
          />
          <RichText
            :rich-text="pageStore.referentialPage.criteriaBlockRightContent"
            class="is-family-secondary column"
          />
        </div>
      </PageSection>
    </div>

    <div class="container">
      <RichText
        v-if="pageStore.referentialPage.pillarStructureLegend"
        :rich-text="pageStore.referentialPage.pillarStructureLegend"
        class="mt-4"
      />
    </div>
    <div class="container mobile-mode">
      <section ref="pillarsRef" class="columns is-multiline mt-2">
        <div
          v-for="pillar of questionnaireStore.pillarsOfMainSurvey"
          :key="pillar.name"
          class="column"
        >
          <QuestionnairePillar
            :name="pillar.name"
            :active="pillar.name === activePillar?.name"
            class="is-clickable"
            @click="onSelectPillar(pillar)"
          />
        </div>
      </section>
      <section v-if="activePillar">
        <QuestionnairePillarReferential
          :pillar="activePillar"
          :color="colorClass"
          :markers="markers"
          :initial-question-id="activeQuestionId"
          :class="`has-text-${colorClass}-dark`"
        >
          <template #criteria="criteriaProps">
            <RichText
              v-if="criteriaProps.criteria.description"
              :rich-text="criteriaProps.criteria.description"
              class="is-family-secondary subtitle mb-2"
              :color="colorClass"
            />
            <Accordion
              v-if="criteriaProps.criteria.definitionIds.length"
              id="definitions"
              :initially-open="true"
            >
              <template #title>
                <h3
                  class="subtitle has-text-weight-bold mb-1"
                  :class="`has-text-${colorClass}-dark`"
                >
                  {{ $t("Definitions") }}
                </h3>
              </template>
              <template #content>
                <div
                  v-for="definitionId of criteriaProps.criteria.definitionIds"
                  :key="definitionId"
                >
                  <p class="has-text-weight-bold">
                    {{ definitionStore.definitionById[definitionId].word }}
                  </p>
                  <RichText
                    :rich-text="
                      definitionStore.definitionById[definitionId].explanation
                    "
                    class="is-family-secondary"
                    :color="colorClass"
                  />
                </div>
              </template>
            </Accordion>
            <template v-if="criteriaProps.criteria.explanatory">
              <Accordion
                v-for="explanatory of criteriaProps.criteria.explanatory"
                :id="explanatory.value.title"
                :key="explanatory.value.title"
                :initially-open="true"
              >
                <template #title>
                  <h3
                    class="subtitle has-text-weight-bold mb-1"
                    :class="`has-text-${colorClass}-dark`"
                  >
                    {{ explanatory.value.title }}
                  </h3>
                </template>
                <template #content>
                  <RichText
                    :rich-text="explanatory.value.description"
                    class="is-family-secondary"
                    :color="colorClass"
                  />
                </template>
              </Accordion>
            </template>
          </template>
          <template #marker="markerProps">
            <RichText
              v-if="markerProps.marker.description"
              :rich-text="markerProps.marker.description"
              class="is-family-secondary subtitle mb-2"
              :color="colorClass"
            />
            <div class="score">
              <div v-for="i in 4" :key="i" class="is-flex mb-1">
                <div class="is-flex">
                  <AnalyticsScore
                    :score="i"
                    :color="colorClass"
                    class="mr-1_5"
                  />
                  <p class="is-family-secondary" style="margin-top: 2px">
                    {{ markerProps.marker["score" + i] }}
                  </p>
                </div>
              </div>
            </div>
          </template>
        </QuestionnairePillarReferential>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"
import { ref, onMounted } from "vue"
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { usePageStore } from "~/stores/pageStore"
import { useDefinitionStore } from "~~/stores/definitionStore"
import { Marker, PillarType } from "~/composables/types"
import { MEDIA_BASE_URL } from "~/composables/api"
import { useI18n } from "vue-i18n"

console.log("### demometre 0")

const i18n = useI18n()
const $t = i18n.t

console.log("### demometre 1")

// definePageMeta({
//   title: $t("DémoMètre"),
//   breadcrumb: $t("DémoMètre"),
// })

const router = useRouter()

const questionnaireStore = useQuestionnaireStore()
const pageStore = usePageStore()
const definitionStore = useDefinitionStore()

if (!pageStore.referentialPage.title) {
  pageStore.getReferentialPage()
}

const activePillar = ref<PillarType>()
const markers = ref<Marker[]>()

const route = useRoute()
const activeQuestionId = computed<number>(() => {
  return parseInt(route.query.question as string)
})

watch(activeQuestionId, () => {
  const pillar =
    questionnaireStore.pillarById[
      questionnaireStore.questionById[activeQuestionId.value]?.pillarId
    ]
  onSelectPillar(pillar)
})

const colorClass = computed(() =>
  activePillar.value ? PillarParams[activePillar.value.name].color : "",
)

const pillarsRef = ref(null)
const explicationRef = ref(null)
onMounted(() => {
  pillarsRef.value.focus()
  explicationRef.value.focus()
})

const onSelectPillar = (pillar) => {
  activePillar.value = pillar
  markers.value = activePillar.value?.markerIds.map(
    (markerId) => questionnaireStore.markerById[markerId],
  )
  router.push({ query: { ...route.query, pillar: pillar.name } })
}

const onDiscoverButtonClick = () => {
  explicationRef.value.scrollIntoView({ behavior: "smooth" })
}
const onRosettePillarClicked = (pillarName) => {
  onSelectPillar(questionnaireStore.getPillarByName(pillarName))
  pillarsRef.value.scrollIntoView({ behavior: "smooth" })
}
const onRosetteMarkerClicked = (markerId) => {
  onRosettePillarClicked(questionnaireStore.markerById[markerId].pillarName)
}

if (activeQuestionId.value) {
  const pillar =
    questionnaireStore.pillarById[
      questionnaireStore.questionById[activeQuestionId.value]?.pillarId
    ]
  onSelectPillar(pillar)
}
</script>

<style scoped lang="sass">
.buttons .button
  height: fit-content

img
  width: 100%
  object-fit: cover

@include touch
  .rosette-menu
    display: none
  .rosette-legend
    display: none
</style>
