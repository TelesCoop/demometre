<template>
  <div class="has-background-shade-100 board-container">
    <p
      v-if="pageStore.participationBoardPage?.title"
      class="title has-text-shade-900 is-4"
    >
      {{ pageStore.participationBoardPage?.title }}
    </p>
    <div class="columns">
      <div
        v-if="showAssessmentInfo"
        class="column is-one-third"
      >
        <h3 class="has-text-weight-bold mb-2">
          {{ $t("Évaluation") }}
        </h3>

        <div class="mb-0_5 has-text-shade-400 is-uppercase is-size-7">
          {{ $t("Territoire") }}
        </div>
        <div class="mb-1_5">
          {{ assessmentStore.currentAssessment?.name }}
        </div>

        <template v-if="assessment?.initiatedBy">
          <div class="mb-0_5 has-text-shade-400 is-uppercase is-size-7">
            {{ $t("Portée par") }}
          </div>
          <div class="mb-1_5">
            {{ assessment.initiatedBy?.firstName }}
            {{ assessment.initiatedBy?.lastName }}
          </div>
        </template>

        <template v-if="assessment.initializedToTheNameOf">
          <div class="mb-0_5 has-text-shade-400 is-uppercase is-size-7">
            {{ $t("Initiateur") }}
          </div>
          <div class="mb-1_5">
            {{ assessment.initializedToTheNameOf }}
          </div>
        </template>

        <div class="mb-0_5 has-text-shade-400 is-uppercase is-size-7">
          {{ $t("Date de lancement") }}
        </div>
        <div class="mb-1_5">
          {{ initializationDate }}
        </div>

        <div class="mb-0_5 has-text-shade-400 is-uppercase is-size-7">
          {{ $t("Nombre de participants") }}
        </div>
        <div class="mb-1">
          {{ assessment.participationCount }}
        </div>
      </div>

      <div class="column">
        <h3 class="has-text-weight-bold mb-0_5">
          {{ $t("Représentativité des participants") }}
        </h3>
        <p class="mb-2 is-size-7">
          {{ $t("Survoler les barres pour afficher les statistiques.") }}
        </p>
        <div class="columns is-multiline">
          <div
            v-for="representativity of assessment.representativities"
            :key="representativity.representativityCriteriaName"
            class="column is-half"
          >
            <ParticipationBoardRepresentativity
              :representativity="representativity"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { Assessment } from "~/composables/types"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { usePageStore } from "~/stores/pageStore"

const props = defineProps({
  assessment: { type: Object as PropType<Assessment>, required: true },
  showAssessmentInfo: { type: Boolean, default: false },
})

const assessmentStore = useAssessmentStore()
const pageStore = usePageStore()
if (!pageStore.participationBoardPage.title) {
  pageStore.getParticipationBoardPage()
}

const initializationDate = computed(() =>
  new Date(props.assessment.initializationDate).toLocaleString("fr-FR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }),
)
</script>

<style scoped lang="sass">
img
  width: 100%
  object-fit: cover

.board-container
  padding: 1.5rem
</style>
