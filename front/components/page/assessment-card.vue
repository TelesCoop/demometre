<template>
  <div :class="`card has-background-${backgroundColor} is-fullheight`">
    <div class="card-content p-2">
      <div class="mb-1_5">
        <p class="is-size-4 has-text-shade-600 has-text-weight-bold">
          {{ props.assessmentType.title }}
        </p>
      </div>
      <div class="content">
        <div
          v-for="caracteristic in caracteristics"
          :key="caracteristic.textKey"
          class="mb-1_5"
        >
          <div
            v-if="props.assessmentType[caracteristic.textKey]"
            class="is-flex mb-0_5"
          >
            <span class="icon mr-1">
              <icon
                size="20"
                :name="caracteristic.icon"
                color="shade-600"
              />
            </span>
            <p class="is-family-secondary is-size-6 has-text-shade-600">
              {{ props.assessmentType[caracteristic.textKey] }}
            </p>
          </div>
        </div>
        <a
          v-if="props.assessmentType.pdfUrl"
          class="button is-shade-600 is-outlined is-rounded is-responsive mb-0_5"
          :href="MEDIA_BASE_URL + props.assessmentType.pdfUrl"
          target="_blank"
        >
          <span class="icon">
            <icon
              size="16"
              name="file-download-line"
            />
          </span>
          <span>{{ props.assessmentType.pdf_button }}</span>
        </a>
        <br>
        <button
          class="button is-shade-600 has-text-white is-rounded is-responsive"
          @click.prevent="letsGo"
        >
          <span class="icon">
            <icon
              size="16"
              name="arrow-right-line"
            />
          </span>
          <span>{{ $t("C'est parti !") }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { MEDIA_BASE_URL } from "~/composables/api"
import { useAssessmentStore } from "~/stores/assessmentStore"
import { AssessmentTypeDetails } from "~~/composables/types"

const props = defineProps({
  assessmentType: {
    type: Object as PropType<AssessmentTypeDetails>,
    required: true,
  },
  backgroundColor: { type: String, required: true },
})

const router = useRouter()
const userStep = useUserStep()
const assessmentStore = useAssessmentStore()

const caracteristics = [
  {
    textKey: "forWho",
    icon: "user",
  },
  {
    textKey: "what",
    icon: "file-text-line",
  },
  {
    textKey: "forWhat",
    icon: "checkbox-line",
  },
  {
    textKey: "results",
    icon: "bar-chart-box-line",
  },
  {
    textKey: "price",
    icon: "money-euro-circle-line",
  },
]

function letsGo() {
  assessmentStore.newAssessment = {
    ...assessmentStore.newAssessment,
    assessmentType: props.assessmentType.assessmentType,
  }
  router.push(userStep.value.url)
}
</script>

<style scoped lang="sass">
// Bulma bugfix
.button.is-shade-600.is-outlined:hover
  color: white
</style>
