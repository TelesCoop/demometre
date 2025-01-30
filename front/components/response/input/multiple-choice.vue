<template>
  <fieldset>
    <legend
      class="is-size-6bis mb-0_75 is-block"
      :class="`has-text-${props.color}-dark`"
    >
      {{ $t("Choisissez entre 1 et {n_choices} réponses").replace("{n_choices}", props.maxMultipleChoices.toString()) }}
    </legend>
    <div
      v-for="(responseChoice, responseChoiceIndex) of props.responseChoices"
      :key="responseChoiceIndex"
      class="mb-1"
    >
      <input
        :id="genInputId(responseChoiceIndex)"
        v-model="answer"
        type="checkbox"
        :name="genInputId()"
        :value="responseChoice.id"
        class="custom-hidden"
        :disabled="
          answer.length >= maxMultipleChoices &&
            answer.indexOf(responseChoice.id) === -1
        "
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
import { computed, PropType } from "vue"
import { ResponseChoice as ResponseChoiceType } from "~/composables/types"
import { useI18n } from "vue-i18n"

const i18n = useI18n()
const $t = i18n.t
const props = defineProps({
  responseChoices: {
    type: Array as PropType<ResponseChoiceType[]>,
    required: true,
  },
  maxMultipleChoices: { type: Number, required: true },
  color: { type: String, required: true },
  questionId: { type: Number, required: true },
})

const answer = defineModel("modelValue", {
  type: Array as PropType<number[]>,
  default: [],
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
