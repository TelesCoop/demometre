<template>
  <div>
    <PageIntro
      :title="pageStore.usagePage.title"
      :subtitle="pageStore.usagePage.tagLine"
      :introduction="pageStore.usagePage.introduction"
      youtube-video-id=""
      :image-url="pageStore.usagePage.introImageUrl"
      :column-distribution="[6, 1, 5]"
    />
    <div class="has-background-shade-250">
      <PageSection
        :title="pageStore.usagePage.stepOfUseTitle"
        :intro="pageStore.usagePage.stepOfUseIntro"
      >
        <div class="columns mb-2 is-variable is-6">
          <div
            v-for="(step, index) in pageStore.usagePage.stepsOfUse"
            :key="index"
            class="column is-one-third"
          >
            <PageStepCard
              :step="step"
              :index="index"
              background-color="white"
            />
          </div>
        </div>
      </PageSection>
    </div>
    <PageSection
      :title="pageStore.usagePage.participateBlockTitle"
      :intro="pageStore.usagePage.participateBlockIntro"
    >
      <div class="columns mb-2">
        <RichText
          :rich-text="pageStore.usagePage.participateLeftParagraph"
          class="is-family-secondary column"
        />
        <RichText
          :rich-text="pageStore.usagePage.participateRightParagraph"
          class="is-family-secondary column"
        />
      </div>
    </PageSection>
    <div class="has-background-shade-250">
      <PageSection
        :title="pageStore.usagePage.startAssessmentBlockTitle"
        :intro="pageStore.usagePage.startAssessmentBlockIntro"
      >
        <div class="columns mb-2">
          <div
            v-for="assessmentType in pageStore.usagePage
              .startAssessmentBlockData"
            :key="assessmentType.id"
            class="column is-one-third"
          >
            <PageAssessmentCard
              :assessment-type="assessmentType"
              background-color="white"
            />
          </div>
        </div>
      </PageSection>
    </div>
    <PageSection
      v-if="trainingStore.trainings.length"
      :title="pageStore.usagePage.trainingBlockTitle"
      :intro="pageStore.usagePage.trainingBlockIntro"
    >
      <div
        style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;"
      >
        <TrainingCard
          v-for="training of trainingStore.trainings"
          :key="training.id"
          :training="training"
        />
      </div>
    </PageSection>
  </div>
</template>

<script setup lang="ts">
import { usePageStore } from "~/stores/pageStore"
import { useTrainingStore } from "~/stores/traningStore"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t

definePageMeta({
  // title: $t("Utilisations possibles"),
  breadcrumb: "Utilisations possibles",
})

const pageStore = usePageStore()
const trainingStore = useTrainingStore()

if (!pageStore.usagePage.title) {
  pageStore.getUsagePage()
}
if (!trainingStore.loaded) {
  trainingStore.getTrainings()
}
</script>

<style scoped lang="sass">
.buttons .button
  height: fit-content
</style>
