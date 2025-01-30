<template>
  <div class="columns">
    <aside class="menu column is-5 mr-2">
      <div
        class="tabs"
        style="margin-top: 6px"
      >
        <ul :class="`is-${color}`">
          <li class="is-active">
            <a
              :class="`has-text-${color}-dark`"
              style="border-bottom-color: currentColor"
            >{{ $t("Marqueurs") }}</a>
          </li>
        </ul>
      </div>
      <ul class="menu-list">
        <li
          v-for="marker of markers"
          :key="marker.id"
        >
          <a
            :class="
              marker === activeMarker && !activeCriteria
                ? activeClass
                : marker.id === hoverMarkerId
                  ? hoverMarkerClass
                  : `has-text-${color}-dark`
            "
            @click="onSelectMarker(marker)"
            @mouseenter="hoverMarkerId = marker.id"
            @mouseleave="hoverMarkerId = null"
          >
            <div class="is-flex is-justify-content-space-between">
              <div class="is-flex">
                <p
                  class="is-size-6bis mr-0_5"
                  style="margin-top: 2px"
                  :class="
                    marker.name === activeMarker?.name && !activeCriteria
                      ? `has-text-${color}-active`
                      : `has-text-${color}-hover`
                  "
                >
                  {{ getConcatenedCodeWithoutPillar(marker.concatenatedCode) }}
                </p>
                <p>{{ wordTitleCase(marker.name) }}</p>
              </div>
              <AnalyticsScore
                v-if="
                  props.showScores &&
                    !isNullOrUndefined(props.scores?.byMarkerId[marker.id])
                "
                :score="getScoreToDisplay(props.scores?.byMarkerId[marker.id])"
                :color="
                  marker.name === activeMarker?.name && !activeCriteria
                    ? `${props.color}-active`
                    : props.color
                "
                :size-circles="9"
                :show-number="false"
                :data-cy="`${marker.name}-score`"
              />
            </div>
          </a>
          <div v-if="marker.name === activeMarker?.name">
            <ul :class="`is-${color}`">
              <li
                v-for="criteria of criterias"
                :key="criteria.id"
              >
                <a
                  :class="
                    criteria === activeCriteria
                      ? activeClass
                      : criteria.id === hoverCriteriaId
                        ? hoverCriteriaClass
                        : ''
                  "
                  @click="onSelectCriteria(criteria)"
                  @mouseenter="hoverCriteriaId = criteria.id"
                  @mouseleave="hoverCriteriaId = null"
                >
                  <div class="is-flex is-justify-content-space-between">
                    <div class="is-flex">
                      <p
                        class="is-size-6bis mr-0_5"
                        style="margin-top: 2px"
                        :class="
                          criteria.name === activeCriteria?.name
                            ? `has-text-${color}-active`
                            : `has-text-${color}-hover`
                        "
                      >
                        {{
                          getConcatenedCodeWithoutPillar(
                            criteria.concatenatedCode
                          )
                        }}
                      </p>
                      <p>
                        {{ criteria.name }}
                        <span v-if="!criteria.hasQuestionsWithScore" class="no-score-tag">{{ $t('non noté') }}</span>
                      </p>
                    </div>
                    <AnalyticsScore
                      v-if="
                        props.showScores &&
                          !isNullOrUndefined(
                            props.scores?.byCriteriaId[criteria.id]
                          )
                      "
                      :score="
                        getScoreToDisplay(
                          props.scores?.byCriteriaId[criteria.id]
                        )
                      "
                      :color="
                        criteria.name === activeCriteria?.name
                          ? `${props.color}-active`
                          : props.color
                      "
                      :size-circles="9"
                      :show-number="false"
                      :data-cy="`${criteria.name}-score`"
                    />
                  </div>
                </a>
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </aside>
    <div class="content column is-7">
      <div v-if="activeCriteria">
        <QuestionnaireReferentialHeaderWithScore
          :color="props.color"
          :title="criteriaTitle"
          :show-score="props.showScores"
          :score="
            getScoreToDisplay(props.scores?.byCriteriaId[activeCriteria.id])
          "
        />
        <slot name="criteria" :criteria="activeCriteria" />
        <div>
          <button
            :class="`button is-${color} is-rounded is-responsive`"
            @click="onReturnToMarkerButtonClick()"
          >
            <span>{{ $t("Revenir au marqueur") }}</span>
          </button>
        </div>
      </div>
      <div v-else-if="activeMarker">
        <QuestionnaireReferentialHeaderWithScore
          :color="props.color"
          :title="markerTitle"
          :show-score="props.showScores"
          :score="getScoreToDisplay(props.scores?.byMarkerId[activeMarker.id])"
        />
        <slot name="marker" :marker="activeMarker" />
        <div>
          <button
            :class="`button is-${color} is-rounded is-responsive mt-2 mr-1`"
            @click="onReturnToPillarButtonClick()"
          >
            <span>{{ $t("Revenir au pilier") }}</span>
          </button>
          <button
            :class="`button is-${color} is-rounded is-responsive mt-2 mr-1 is-outlined has-text-${color}-dark`"
            @click="onFirstCriteriaButtonClick()"
          >
            <span>{{ $t("Premier critère") }}</span>
            <span class="icon">
              <icon
                name="arrow-right-line"
                size="10"
                class="icon"
              />
            </span>
          </button>
        </div>
      </div>
      <div v-else>
        <QuestionnaireReferentialHeaderWithScore
          :color="props.color"
          :title="wordTitleCase(pillar.name)"
          :show-score="props.showScores"
          :score="getScoreToDisplay(props.scores?.byPillarId[pillar.id])"
        />
        <RichText
          v-if="pillar.description"
          :rich-text="pillar.description"
          class="is-family-secondary subtitle mb-2"
          :color="props.color"
        />
        <slot name="pillar" :pillar="pillar" />
        <div>
          <button
            :class="`button is-${color} is-rounded is-responsive is-outlined has-text-${color}-dark`"
            @click="onFirstMarkerButtonClick()"
          >
            <span>{{ $t("Premier marqueur") }}</span>
            <span class="icon">
              <icon
                name="arrow-right-line"
                size="10"
                class="icon"
              />
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, PropType } from "vue"
import { wordTitleCase } from "~/utils/util"
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { Marker, Criteria, Scores } from "~/composables/types"
import { getScoreToDisplay } from "~/utils/scores"
import { isNullOrUndefined } from "assets/utils"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
const questionnaireStore = useQuestionnaireStore()

const props = defineProps({
  assessmentType: { type: String, required: false },
  pillar: { type: Object, required: true },
  color: { type: String, required: true },
  markers: {
    type: Array,
    required: false,
    default() {
      return []
    },
  },
  initialQuestionId: {
    type: Number,
    required: false,
    default: undefined,
  },
  showScores: { type: Boolean, default: false },
  scores: {
    type: Object as PropType<Scores>,
    required: false,
    default() {
      return undefined
    },
  },
})
const getCriteriasOfActiveMarker = () => {
  return activeMarker.value?.criteriaIds
    .filter((criteriaId) => questionnaireStore.isCriteriaRelevantForAssessmentType(props.assessmentType, criteriaId))
    .map((criteriaId) => questionnaireStore.criteriaById[criteriaId])
}

const getCriteriaOfQuestionId = () => {
  return questionnaireStore.criteriaById[
    questionnaireStore.questionById[props.initialQuestionId]?.criteriaId
  ]
}

const activeCriteria = ref<Criteria>(getCriteriaOfQuestionId())
const activeMarker = ref<Marker>(
  questionnaireStore.markerById[activeCriteria.value?.markerId],
)
const criterias = ref<Criteria[]>(getCriteriasOfActiveMarker())
const hoverMarkerId = ref<number>()
const hoverCriteriaId = ref<number>()

const markerTitle = computed<string>(() =>
  activeMarker.value ? wordTitleCase(activeMarker.value.name) : "",
)
const criteriaTitle = computed<string>(() =>
  activeCriteria.value ? wordTitleCase(activeCriteria.value.name) : "",
)

watch(
  () => props.markers,
  () => {
    activeMarker.value = null
    activeCriteria.value = null
  },
)

watch(
  () => props.initialQuestionId,
  () => {
    activeCriteria.value = getCriteriaOfQuestionId()
    activeMarker.value =
      questionnaireStore.markerById[activeCriteria.value?.markerId]
    criterias.value = getCriteriasOfActiveMarker()
  },
)

const onSelectMarker = (marker) => {
  activeMarker.value = marker
  criterias.value = getCriteriasOfActiveMarker()
  activeCriteria.value = null
}
const onSelectCriteria = (criteria) => {
  activeCriteria.value = criteria
}

const activeClass = computed(() => {
  return `has-background-${props.color} has-text-${props.color}-dark`
})

const hoverMarkerClass = computed(() => {
  return `has-background-${props.color}-light has-text-black`
})
const hoverCriteriaClass = computed(() => {
  return `has-background-${props.color}-light has-text-black`
})

const getConcatenedCodeWithoutPillar = (code) => {
  return code.substring(1).replace(/^\./, "")
}

const onFirstMarkerButtonClick = () => {
  const firstMarker = props.markers[0]
  onSelectMarker(firstMarker)
}
const onFirstCriteriaButtonClick = () => {
  const firstCriteria = criterias.value[0]
  onSelectCriteria(firstCriteria)
}

const onReturnToPillarButtonClick = () => {
  activeMarker.value = null
}
const onReturnToMarkerButtonClick = () => {
  activeCriteria.value = null
}
</script>

<style scoped lang="sass">
.tabs ul
  border-bottom-color: var(--color) !important

.menu-list li ul
  border-left-color: var(--color) !important
.no-score-tag
  background: lightgray
  color: #585858
  font-size: 0.75em
  padding: 0.25rem 0.5rem
  border-radius: 0.5rem
  white-space: nowrap
</style>
