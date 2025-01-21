<template>
  <div class="my-1_5">
    <ResponseInputPercentage
      v-if="question.type === QuestionType.PERCENTAGE"
      v-model="answer"
      :color="props.color"
      :question-id="question.id"
    />
    <ResponseInputNumber
      v-if="question.type === QuestionType.NUMBER"
      v-model="answer"
      :color="props.color"
      :question-id="question.id"
      :min="question.minNumberValue"
      :max="question.maxNumberValue"
      :step="question.stepNumberValue"
    />
    <ResponseInputUniqueChoice
      v-else-if="question.type === QuestionType.UNIQUE_CHOICE"
      v-model="answer"
      :response-choices="question.responseChoices"
      :color="props.color"
      :question-id="question.id"
    />
    <ResponseInputMultipleChoice
      v-else-if="question.type === QuestionType.MULTIPLE_CHOICE"
      v-model="answer"
      :response-choices="question.responseChoices"
      :max-multiple-choices="
        question.maxMultipleChoices || question.responseChoices.length
      "
      :color="props.color"
      :question-id="question.id"
    />
    <ResponseInputBinary
      v-else-if="question.type === QuestionType.BOOLEAN"
      v-model="answer"
      :color="props.color"
      :question-id="question.id"
    />
    <ResponseInputScale
      v-else-if="question.type === QuestionType.CLOSED_WITH_SCALE"
      v-model="answer"
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
import { computed, PropType } from "vue"
import {
  getQuestionResponseValue,
  toQuestionResponseValue,
} from "~/utils/question-response"

const props = defineProps({
  question: { type: Object as PropType<Question>, required: true },
  color: { type: String, required: true },
})

const value = defineModel("modelValue", {
  type: Object as PropType<QuestionResponseValue | undefined>,
})

const answer = computed({
  get: () => getQuestionResponseValue(value.value, props.question.type),
  set: (newValue) => {
    value.value = {
      ...value.value,
      ...toQuestionResponseValue(newValue, props.question.type),
    }
  },
})
</script>

<style scoped lang="sass"></style>
