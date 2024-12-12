<template>
  <div class="score">
    <b
      v-if="props.showNumber"
      class="score-number"
      :class="props.sizeNumberClass"
    >{{ score }}</b>
    <span
      v-for="i in maxScore"
      :key="i"
      :class="
        i <= score
          ? `has-background-${color}`
          : `has-background-transparent has-border-${color}`
      "
      class="score-circle"
      :style="`width: ${props.sizeCircles}px; height: ${props.sizeCircles}px`"
    />
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  color: { type: String, required: true },
  score: { type: Number, required: true },
  sizeCircles: { type: Number, default: 12 },
  sizeNumberClass: { type: String, default: "is-size-5" },
  showNumber: { type: Boolean, default: true },
  maxScore: { type: Number, default: 4 },
})
</script>

<style scoped lang="sass">
.score
  display: block
  min-width: fit-content
  &-number
    vertical-align: middle
    margin-right: 0.5rem

  &-circle
    border-radius: 100%
    margin: 2px
    display: inline-block
    vertical-align: middle
@include until(430px)
  .score
    &-number
      margin-right: 0.2rem
      font-size: 1em !important
    &-circle
      margin: 1px
</style>
