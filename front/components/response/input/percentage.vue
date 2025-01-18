<template>
  <div class="control has-icons-right percentage ml-0_5 mb-4">
    <input
      :id="`$question-${props.questionId}-percentage`"
      v-model="answer"
      type="number"
      min="0"
      max="100"
      data-cy="percentage-input"
      class="input"
      :class="`has-background-${props.color}-light has-border-${props.color}-dark has-text-${props.color}-dark`"
      :placeholder="placeholder"
    >
    <i
      class="icon is-small is-right"
      :class="`has-text-${props.color}-dark`"
    >
      <span>%</span>
    </i>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  color: { type: String, required: true },
  questionId: { required: true, type: Number },
  placeholder: { type: String, default: "50" },
})

const answer = defineModel("modelValue", {
  type: Number,
})
</script>

<style scoped lang="sass">
.percentage
  width: min-content
  min-width: 6rem
</style>
