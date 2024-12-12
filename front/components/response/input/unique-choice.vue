<template>
  <fieldset>
    <legend
      class="is-size-6bis mb-0_75 is-block"
      :class="`has-text-${props.color}-dark`"
    >
      <slot name="legend">
        {{ $t("Choisissez une réponse.") }}
      </slot>
    </legend>
    <div
      v-for="(responseChoice, responseChoiceIndex) of props.responseChoices"
      :key="responseChoiceIndex"
      class="mb-1"
    >
      <input
        :id="genInputId(responseChoiceIndex)"
        v-model="answer"
        type="radio"
        :name="genInputId()"
        :value="responseChoice.id"
        class="custom-hidden"
        @click="unCheck(responseChoice.id)"
      >
      <label :for="genInputId(responseChoiceIndex)">
        <ResponseChoice
          :for="genInputId(responseChoiceIndex)"
          :response-choice="responseChoice"
          :response-choice-index="responseChoiceIndex"
          :selected="isResponseChoiceSelected(responseChoice.id)"
          :color="props.color"
        />
      </label>
    </div>
  </fieldset>
</template>

<script setup lang="ts">
import { PropType } from "vue"
import { ResponseChoice as ResponseChoiceType } from "~/composables/types"

const props = defineProps({
  responseChoices: {
    type: Array as PropType<ResponseChoiceType[]>,
    required: true,
  },
  color: { type: String, required: true },
  questionId: { type: [Number, String], required: true },
})

const previousAnswer = ref()
const answer = defineModel("modelValue", {
  type: Number,
  default: null,
  required: false,
})
const isResponseChoiceSelected = computed(
  () => (responseChoiceId: number) => responseChoiceId === answer.value,
)

function genInputId(responseChoiceIndex = null) {
  if (responseChoiceIndex === null) {
    return `question-${props.questionId}-unique-choice`
  }
  return `question-${props.questionId}-unique-choice-${responseChoiceIndex}`
}

function unCheck(responseChoiceId: number) {
  if (responseChoiceId === previousAnswer.value) {
    answer.value = undefined
  }
  previousAnswer.value = responseChoiceId
}
</script>
