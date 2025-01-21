<template>
  <div class="container">
    <NuxtLink
      class="button is-white is-rounded"
      to="."
    >
      <span class="icon">
        <icon
          size="20"
          name="arrow-left-line"
        />
      </span>
      <span> {{ $t("Revenir à l'atelier") }} </span>
    </NuxtLink>
    <div class="section">
      <PageTitle :title="`${workshop?.name} - réponses papier`" />
      <p class="is-size-4">
        {{ $t("Saisissez les réponses des participants aux évaluations papier.") }}
      </p>
      <p
        v-if="!activePillar"
        class="is-size-4"
      >
        {{ $t("Choisissez un pillier pour commencer.") }}
      </p>

      <div class="container">
        <section
          ref="pillarsRef"
          class="columns is-multiline mt-4"
        >
          <div
            v-for="pillar of questionnaireStore.pillarsOfSurvey(
              assessment.surveyId,
            )"
            :key="pillar.name"
            class="column"
          >
            <QuestionnairePillar
              :name="pillar.name"
              :active="pillar.name === activePillar?.name"
              style="cursor: pointer"
              @click="onSelectPillar(pillar)"
            />
          </div>
        </section>
        <section v-if="activePillar">
          <QuestionnairePillarAnimatorResponses
            :pillar="activePillar"
            :color="colorClass"
            :workshop-id="workshopId"
          />
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useQuestionnaireStore } from "~/stores/questionnaireStore"
import { Marker, PillarType, Workshop } from "~/composables/types"
import { useWorkshopStore } from "~/stores/workshopStore"
import { usePageStore } from "~/stores/pageStore"
import { useUserStore } from "~/stores/userStore"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { useAssessmentIsReady } from "~/composables/useAssessmentIsReady"

definePageMeta({
  title: "Réponses",
  breadcrumb: "Réponses",
})

const assessmentStore = useAssessmentStore()
const questionnaireStore = useQuestionnaireStore()
const pageStore = usePageStore()
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()
const workshopId: number = +route.params.workshopId
const workshopStore = useWorkshopStore()

await useAssessmentIsReady()

const workshop = computed<Workshop>(
  () => workshopStore.workshopById[workshopId],
)
const assessment = assessmentStore.currentAssessment
if (!pageStore.animatorPage.listWorkshopsTitle) {
  pageStore.getAnimatorPage()
}
if (!workshop.value) {
  workshopStore.getWorkshop(workshopId)
}

if (!userStore.isLoggedIn) {
  navigateTo(`/login`)
}

const activePillar = ref<PillarType>()
const markers = ref<Marker[]>()

const colorClass = computed(() =>
  activePillar.value ? PillarParams[activePillar.value.name].color : "",
)
const onSelectPillar = (pillar: PillarType) => {
  activePillar.value = pillar
  markers.value = activePillar.value?.markerIds.map(
    (markerId) => questionnaireStore.markerById[markerId],
  )
  router.replace({ path: "reponses", query: { pillar: pillar.name } })
}
</script>

<style scoped lang="sass"></style>
