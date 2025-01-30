<template>
  <div class="my-1_5">
    <ResponseInputPercentage
      v-if="question.type === QuestionType.PERCENTAGE"
      :color="props.color"
      :question-id="question.id"
      placeholder=""
    />
    <ResponseInputNumber
      v-if="question.type === QuestionType.NUMBER"
      :color="props.color"
      :question-id="question.id"
      :min="question.minNumberValue"
      :max="question.maxNumberValue"
      :step="question.stepNumberValue"
    />
    <ResponsePaperInputUniqueChoice
      v-else-if="question.type === QuestionType.UNIQUE_CHOICE"
      :response-choices="question.responseChoices"
      :color="props.color"
      :question-id="question.id"
    />
    <ResponsePaperInputMultipleChoice
      v-else-if="question.type === QuestionType.MULTIPLE_CHOICE"
      :response-choices="question.responseChoices"
      :max-multiple-choices="
        question.maxMultipleChoices || question.responseChoices.length
      "
      :color="props.color"
      :question-id="question.id"
    />
    <ResponsePaperInputBinary
      v-else-if="question.type === QuestionType.BOOLEAN"
      :color="props.color"
      :question-id="question.id"
    />
    <ResponsePaperInputScale
      v-else-if="question.type === QuestionType.CLOSED_WITH_SCALE"
      :categories="question.categories"
      :color="props.color"
      :response-choices="question.responseChoices"
    />
  </div>
</template>

<script setup lang="ts">
import {
  Question,
  QuestionResponseValue,
  QuestionType,
} from "~/composables/types"
import { PropType } from "vue"

const props = defineProps({
  question: { type: Object as PropType<Question>, required: true },
  color: { type: String, required: true },
})

defineModel("modelValue", {
  type: Object as PropType<QuestionResponseValue | undefined>,
})
</script>

<style scoped lang="sass"></style>
