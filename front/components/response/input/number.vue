<template>
  <div class="control number mb-4">
    <input
      :id="`$question-${props.questionId}-number`"
      v-model="answer"
      :readonly="readOnly"
      data-cy="number-input"
      type="number"
      :min="min"
      :max="max"
      :step="step"
      class="input"
      :class="`has-background-${props.color}-light has-border-${props.color}-dark has-text-${props.color}-dark`"
    >
  </div>
</template>

<script setup lang="ts">
import { PropType } from "vue"

const props = defineProps({
  color: { type: String, required: true },
  questionId: { required: true, type: Number },
  min: { type: Number as PropType<number | null>, default: null },
  max: { type: Number as PropType<number | null>, default: null },
  step: { type: Number as PropType<number | null>, required: true },
  readOnly: { type: Boolean, default: false },
})

const answer = defineModel("modelValue", {
  type: Number,
})
</script>

<style scoped lang="sass">
.number
  width: min-content
  min-width: 10rem
</style>
