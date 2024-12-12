<template>
  <div
    :class="{ 'is-dashed': index % fullLineModulo !== 0 }"
    :style="
      getLeftStyle(
        index,
        percentageOfSpaceAlreadyTaken,
        totalLine,
        gapSize,
        percentageSize,
        leftBaseMargin
      )
    "
  />
</template>

<script setup lang="ts">
import { getLeftStyle } from "assets/utils/choice-question-chart"

defineProps({
  index: { type: Number, required: true },
  color: { type: String, required: true },
  totalLine: { type: Number, required: true },
  percentageOfSpaceAlreadyTaken: { type: Number, required: true },
  gapSize: { type: Number, required: true },
  fullLineModulo: { type: Number, required: true },
  percentageSize: { type: Number, required: true },
  leftBaseMargin: { type: Number, default: 1 },
})
</script>

<style scoped lang="sass">
.is-dashed
  border-left-style: dashed
  border-left-color: var(--color)
</style>
