<template>
  <fieldset>
    <legend
      class="is-size-6bis mb-0_75 is-block"
      :class="`has-text-${props.color}-dark`"
    >
      {{ $t("Sélectionnez le ou les process participatifs auxquels vous avez participé") }}
    </legend>
    <div
      v-for="(participativeProcess, participativeProcessIndex) of participativeProcesses"
      :key="participativeProcess.id"
      class="mb-1"
    >
      <input
        :id="genInputId(participativeProcess.id)"
        v-model="answer"
        type="checkbox"
        :name="genInputId()"
        :value="participativeProcess.id"
        class="custom-hidden"
      >
      <label :for="genInputId(participativeProcess.id)">
        <ResponseChoice
          :for="genInputId(participativeProcess.id)"
          :response-choice="fakeResponseChoice(participativeProcess)"
          :response-choice-index="participativeProcessIndex"
          :selected="isResponseChoiceSelected(participativeProcess.id)"
          :color="props.color"
        />
      </label>
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import { computed, PropType } from "vue"
import {ParticipationParticipativeProcess} from "~/composables/types"
import {useAssessmentStore} from "~/stores/assessmentStore"

const props = defineProps({
  maxMultipleChoices: { type: Number, required: true },
  color: { type: String, required: true },
  questionId: { type: Number, required: true },
})

const assessmentStore = useAssessmentStore()

const participativeProcesses = computed(() => {
  return assessmentStore.currentAssessment?.participativeProcesses || []
})

const answer = defineModel("modelValue", {
  type: Array as PropType<number[]>,
  default: [],
})
const fakeResponseChoice = computed(() => {
  return (participaptiveProcess: ParticipationParticipativeProcess) => {
    return {
      responseChoice: `${participaptiveProcess.category.name} - ${participaptiveProcess.name}`,
      description: '',
    }
  }
})

const isResponseChoiceSelected = computed(
  () => (responseChoiceId: number) => answer.value?.includes(responseChoiceId),
)

function genInputId(responseChoiceIndex = null) {
  if (responseChoiceIndex === null) {
    return `question-${props.questionId}-multiple-choice`
  }
  return `question-${props.questionId}-multiple-choice-${responseChoiceIndex}`
}
</script>
