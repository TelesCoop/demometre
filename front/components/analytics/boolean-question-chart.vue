<template>
  <div class="boolean-chart">
    <div class="boolean-chart-title is-size-5 mb-0_5">
      <span :class="`has-text-${color}-hover`">
        {{ data.true.label }}
        <strong :class="`has-text-${color}-hover`">{{ truePercentage }}%</strong>
      </span>
      <span :class="`has-text-${color}`">
        <strong :class="`has-text-${color}`">{{ falsePercentage }}%</strong>
        {{ data.false.label }}
      </span>
    </div>
    <div class="boolean-chart-bar" :class="`has-background-${color}`">
      <span
        class="boolean-chart-bar-load"
        :class="`has-background-${color}-hover`"
        :style="`width: ${truePercentage}%;`"
      />
      <span
        class="boolean-chart-bar-center-line"
        :class="`has-background-${color}-dark`"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { getPercentage } from "assets/utils/percentage"

const props = defineProps({
  data: { type: Object, required: true },
  color: { type: String, required: true },
})
const truePercentage = getPercentage(props.data.true.value, props.data.count)
const falsePercentage = getPercentage(props.data.false.value, props.data.count)
</script>

<style scoped lang="sass">
.boolean-chart
  &-title
    display: flex
    justify-content: space-between
    align-items: center
  &-bar
    position: relative
    height: 24px
    width: 100%
    &-load
      display: flex
      height: 100%
    &-center-line
      position: absolute
      top: 50%
      left: 50%
      width: 1px
      height: 36px
      transform: translate(-50%, -50%)
</style>
