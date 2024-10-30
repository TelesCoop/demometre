<template>
  <div class="result-image-container">
    <div class="container page-height">
      <section class="columns section">
        <div class="column is-5">
          <PageTitle
            :title="pageStore.resultsPage.title"
            :subtitle="
              assessmentStore.canSeeResultsAssessments.length
                ? pageStore.resultsPage.tagLine
                : pageStore.resultsPage.tagLineNoResults
            "
          />
          <RichText
            :rich-text="pageStore.resultsPage.introduction"
            class="is-family-secondary"
          />
          <div v-if="assessmentStore.canSeeResultsAssessments.length">
            <v-select
              v-model="assessmentSelected"
              label="name"
              :options="assessmentStore.canSeeResultsAssessments"
            />
            <button
              class="button is-rounded is-shade-600 is-outlined mt-2"
              type="button"
              :disabled="!assessmentSelected"
              @click.prevent="seeResults()"
            >
              <span class="icon">
                <icon
                  size="16"
                  name="bar-chart-box-line"
                />
              </span>
              <span>{{ $t("Voir les résultats") }}</span>
            </button>
          </div>
          <div
            v-else
            class="notification"
          >
            <template v-if="assessmentStore.assessmentsLoaded">
              {{ $t("Aucun résultat n'est actuellement visible") }}
            </template>
            <template v-else>
              {{ $t("chargement...") }}
            </template>
          </div>
        </div>
      </section>
    </div>
    <div
      v-if="pageStore.resultsPage.introImageUrl"
      class="result-image is-hidden-mobile"
      :style="`background-image: url(${
        MEDIA_BASE_URL + pageStore.resultsPage.introImageUrl
      })`"
    />
  </div>
</template>

<script setup lang="ts">
import { usePageStore } from "~/stores/pageStore"
import { MEDIA_BASE_URL } from "~/composables/api"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { Assessment } from "~/composables/types"
import vSelect from "vue-select"

definePageMeta({
  title: "Résultats",
  breadcrumb: "Résultats",
})

const pageStore = usePageStore()
const assessmentStore = useAssessmentStore()
const router = useRouter()

if (!pageStore.resultsPage.title) {
  pageStore.getResultsPage()
}
if (!assessmentStore.assessmentsWithResultsLoaded) {
  assessmentStore.getAssesmentsWithPublicatedResults()
}

const assessmentSelected = ref<Assessment>()

const seeResults = () => {
  router.push(`/resultats/${assessmentSelected.value.id}`)
}
</script>

<style scoped lang="sass">
.page-height
  min-height: 580px

@include touch
  .page-height
    min-height: fit-content

.result-image
  position: absolute
  top: -4rem
  right: 0
  width: 55%
  height: 150%
  background-repeat: repeat
  z-index: -1

  &-container
    position: relative
</style>
